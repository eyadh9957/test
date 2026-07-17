import aiohttp
import asyncio
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class QuestCompleter:
    """Handle quest completion using Discord token."""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        self.api_base = 'https://discord.com/api/v10'
    
    async def get_quests(self) -> List[Dict]:
        """Fetch all available quests."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.api_base}/users/@me/quests',
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        quests = data.get('quests', [])
                        logger.info(f'Fetched {len(quests)} quests')
                        return quests
                    else:
                        logger.error(f'Error fetching quests: {response.status}')
                        return []
        except Exception as e:
            logger.error(f'Error fetching quests: {e}')
            return []
    
    async def get_active_quests(self) -> List[Dict]:
        """Fetch active (incomplete) quests only."""
        try:
            quests = await self.get_quests()
            active_quests = [q for q in quests if not q.get('completed', False)]
            logger.info(f'Found {len(active_quests)} active quests')
            return active_quests
        except Exception as e:
            logger.error(f'Error getting active quests: {e}')
            return []
    
    async def complete_quest(self, quest_id: str) -> bool:
        """Complete a specific quest."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.api_base}/quests/{quest_id}/complete',
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status in [200, 204]:
                        logger.info(f'Quest {quest_id} completed successfully')
                        return True
                    else:
                        logger.warning(f'Failed to complete quest {quest_id}: {response.status}')
                        return False
        except Exception as e:
            logger.error(f'Error completing quest {quest_id}: {e}')
            return False
    
    async def complete_all_quests(self) -> int:
        """Complete all active quests."""
        completed_count = 0
        try:
            active_quests = await self.get_active_quests()
            
            for quest in active_quests:
                quest_id = quest.get('id')
                quest_name = quest.get('name', 'Unknown')
                
                success = await self.complete_quest(quest_id)
                if success:
                    completed_count += 1
                    logger.info(f'Completed quest: {quest_name}')
                    await asyncio.sleep(1)  # Rate limiting
                else:
                    logger.warning(f'Failed to complete quest: {quest_name}')
            
            logger.info(f'Completed {completed_count} quests total')
            return completed_count
        except Exception as e:
            logger.error(f'Error in complete_all_quests: {e}')
            return completed_count
    
    async def auto_complete_loop(self, interval: int = 3600):
        """Continuously complete quests at regular intervals.
        
        Args:
            interval: Time in seconds between completion cycles (default 1 hour)
        """
        logger.info(f'Starting auto-complete loop with {interval}s interval')
        
        try:
            while True:
                logger.info('Running quest completion cycle...')
                await self.complete_all_quests()
                logger.info(f'Next completion cycle in {interval}s')
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info('Auto-complete loop cancelled')
        except Exception as e:
            logger.error(f'Error in auto_complete_loop: {e}')
