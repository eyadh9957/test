import aiohttp
import asyncio
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class QuestCompleter:
    """Handle quest completion and orb claiming using Discord token."""
    
    def __init__(self, user_token: str):
        self.user_token = user_token
        self.headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.api_base = 'https://discord.com/api/v10'
    
    async def get_user_info(self) -> Optional[Dict]:
        """Get current user information to verify token."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.api_base}/users/@me',
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f'User info fetched: {data.get("username")}')
                        return data
                    else:
                        logger.error(f'Failed to fetch user info: {response.status}')
                        return None
        except Exception as e:
            logger.error(f'Error fetching user info: {e}')
            return None
    
    async def validate_token(self) -> bool:
        """Validate if the token is valid."""
        user_info = await self.get_user_info()
        return user_info is not None
    
    async def get_quests(self) -> List[Dict]:
        """Fetch all available quests from user's account."""
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
                    elif response.status == 401:
                        logger.error('Invalid token - unauthorized')
                        return []
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
                endpoints = [
                    f'{self.api_base}/quests/{quest_id}/complete',
                    f'{self.api_base}/users/@me/quests/{quest_id}/complete',
                ]
                
                for endpoint in endpoints:
                    try:
                        async with session.post(
                            endpoint,
                            headers=self.headers,
                            timeout=aiohttp.ClientTimeout(total=30)
                        ) as response:
                            if response.status in [200, 204]:
                                logger.info(f'Quest {quest_id} completed successfully')
                                return True
                    except:
                        continue
                
                logger.warning(f'Failed to complete quest {quest_id}')
                return False
        except Exception as e:
            logger.error(f'Error completing quest {quest_id}: {e}')
            return False
    
    async def claim_orbs(self) -> int:
        """Claim all available orbs from completed quests."""
        orbs_claimed = 0
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f'{self.api_base}/users/@me/orbs',
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        pending_orbs = data.get('pending', [])
                        
                        for orb in pending_orbs:
                            orb_id = orb.get('id')
                            try:
                                async with session.post(
                                    f'{self.api_base}/users/@me/orbs/{orb_id}/claim',
                                    headers=self.headers,
                                    timeout=aiohttp.ClientTimeout(total=30)
                                ) as claim_response:
                                    if claim_response.status in [200, 204]:
                                        orbs_claimed += 1
                                        logger.info(f'Claimed orb {orb_id}')
                                        await asyncio.sleep(0.5)
                            except Exception as e:
                                logger.error(f'Error claiming orb {orb_id}: {e}')
                        
                        logger.info(f'Claimed {orbs_claimed} orbs total')
                        return orbs_claimed
        except Exception as e:
            logger.error(f'Error in claim_orbs: {e}')
            return orbs_claimed
    
    async def complete_all_quests(self) -> Dict:
        """Complete all active quests and claim orbs."""
        stats = {
            'quests_completed': 0,
            'orbs_claimed': 0,
            'success': False
        }
        
        try:
            logger.info('Starting quest completion cycle...')
            
            active_quests = await self.get_active_quests()
            logger.info(f'Found {len(active_quests)} active quests to complete')
            
            for quest in active_quests:
                quest_id = quest.get('id')
                quest_name = quest.get('name', 'Unknown')
                
                success = await self.complete_quest(quest_id)
                if success:
                    stats['quests_completed'] += 1
                    logger.info(f'Completed quest: {quest_name}')
                    await asyncio.sleep(0.5)
                else:
                    logger.warning(f'Failed to complete quest: {quest_name}')
            
            logger.info('Claiming orbs...')
            orbs_claimed = await self.claim_orbs()
            stats['orbs_claimed'] = orbs_claimed
            
            stats['success'] = True
            logger.info(f'Cycle complete: {stats["quests_completed"]} quests, {orbs_claimed} orbs')
            return stats
        except Exception as e:
            logger.error(f'Error in complete_all_quests: {e}')
            return stats
    
    async def auto_complete_loop(self, interval: int = 300):
        """Continuously complete quests and claim orbs at regular intervals.
        
        Args:
            interval: Time in seconds between completion cycles (default 5 minutes)
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
