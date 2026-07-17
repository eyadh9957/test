import discord
from discord import app_commands
from discord.ext import commands, tasks
import logging
from datetime import datetime
from utils.quest_completer import QuestCompleter
from bot.database import Database
import asyncio

logger = logging.getLogger(__name__)

class QuestCommands(commands.Cog):
    """Quest completion commands for all server members."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()
        self.active_sessions = {}  # {user_id: {'completer': QuestCompleter, 'task': asyncio.Task, 'quests_completed': int}}
        self.db = Database('sqlite:///./quest_bot.db')
    
    @app_commands.command(name='link', description='Link your Discord token to auto-complete quests')
    async def link(self, interaction: discord.Interaction):
        """Link user's Discord token for quest completion.
        
        This is a multi-user bot where each member links their own token.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            user_id = str(interaction.user.id)
            username = interaction.user.name
            
            # Create user in database
            self.db.create_user(user_id, username)
            
            embed = discord.Embed(
                title='✅ Token Linked',
                description='Your Discord account has been linked!\nYou can now auto-complete quests.',
                color=discord.Color.green()
            )
            embed.add_field(name='Username', value=username, inline=True)
            embed.add_field(name='Status', value='🟢 Linked', inline=True)
            embed.add_field(name='Next Step', value='Use `/start` to begin quest completion', inline=False)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f'User {username} ({user_id}) linked their token')
        except Exception as e:
            logger.error(f'Error in link: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
    
    @app_commands.command(name='start', description='Start auto-completing YOUR quests')
    async def start(self, interaction: discord.Interaction):
        """Start auto-completing quests for the user."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            username = interaction.user.name
            
            # Check if already running
            if user_id in self.active_sessions:
                embed = discord.Embed(
                    title='⚠️ Already Running',
                    description='Quest completion is already running for you',
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Get user's token from database
            user_obj = self.db.get_user(user_id)
            if not user_obj or not user_obj.discord_token:
                embed = discord.Embed(
                    title='❌ Token Not Linked',
                    description='Please link your Discord token first using `/link`',
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Initialize quest completer with user's token
            completer = QuestCompleter(user_obj.discord_token)
            
            # Create completion task
            task = asyncio.create_task(completer.auto_complete_loop(interval=300))  # 5 minute interval
            
            # Store session
            self.active_sessions[user_id] = {
                'completer': completer,
                'task': task,
                'quests_completed': 0,
                'started_at': datetime.utcnow(),
                'username': username
            }
            
            embed = discord.Embed(
                title='▶️ Quest Completion Started',
                description='Started auto-completing your quests',
                color=discord.Color.green()
            )
            embed.add_field(name='Status', value='🟢 Running', inline=True)
            embed.add_field(name='Quests Completed', value='0', inline=True)
            embed.add_field(name='User', value=interaction.user.mention, inline=False)
            embed.add_field(name='Interval', value='Every 5 minutes', inline=True)
            embed.add_field(name='Tip', value='Use `/progress` to check your stats', inline=True)
            
            await interaction.followup.send(embed=embed)
            logger.info(f'{username} ({user_id}) started quest completion')
        except Exception as e:
            logger.error(f'Error in start: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='stop', description='Stop auto-completing YOUR quests')
    async def stop(self, interaction: discord.Interaction):
        """Stop auto-completing quests."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            username = interaction.user.name
            
            # Check if session exists
            if user_id not in self.active_sessions:
                embed = discord.Embed(
                    title='⚠️ No Active Session',
                    description='Quest completion is not running for you',
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Stop the session
            session = self.active_sessions[user_id]
            session['task'].cancel()
            quests_completed = session.get('quests_completed', 0)
            del self.active_sessions[user_id]
            
            embed = discord.Embed(
                title='⏹️ Quest Completion Stopped',
                description='Stopped auto-completing your quests',
                color=discord.Color.red()
            )
            embed.add_field(name='Status', value='🔴 Stopped', inline=True)
            embed.add_field(name='Quests Completed This Session', value=str(quests_completed), inline=True)
            
            await interaction.followup.send(embed=embed)
            logger.info(f'{username} ({user_id}) stopped quest completion')
        except Exception as e:
            logger.error(f'Error in stop: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='complete_now', description='Complete all YOUR quests immediately')
    async def complete_now(self, interaction: discord.Interaction):
        """Manually trigger quest completion immediately."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            username = interaction.user.name
            
            # Get user's token from database
            user_obj = self.db.get_user(user_id)
            if not user_obj or not user_obj.discord_token:
                embed = discord.Embed(
                    title='❌ Token Not Linked',
                    description='Please link your Discord token first using `/link`',
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Complete quests immediately
            completer = QuestCompleter(user_obj.discord_token)
            completed_count = await completer.complete_all_quests()
            
            # Update session if running
            if user_id in self.active_sessions:
                self.active_sessions[user_id]['quests_completed'] += completed_count
            
            embed = discord.Embed(
                title='✅ Quests Completed',
                description=f'Successfully completed {completed_count} quests',
                color=discord.Color.green()
            )
            embed.add_field(name='Quests', value=str(completed_count), inline=True)
            embed.add_field(name='Rewards', value=f'{completed_count * 100} XP', inline=True)
            
            await interaction.followup.send(embed=embed)
            logger.info(f'{username} ({user_id}) manually completed {completed_count} quests')
        except Exception as e:
            logger.error(f'Error in complete_now: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='progress', description='View YOUR quest completion progress')
    async def progress(self, interaction: discord.Interaction):
        """View quest completion progress for the user."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            session = self.active_sessions.get(user_id)
            
            if session:
                quests_completed = session.get('quests_completed', 0)
                started_at = session.get('started_at')
                duration = datetime.utcnow() - started_at
                hours, remainder = divmod(int(duration.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = f'{hours}h {minutes}m {seconds}s'
                status = 'Running'
                status_emoji = '🟢'
            else:
                quests_completed = 0
                status = 'Not Running'
                status_emoji = '🔴'
                duration_str = 'N/A'
            
            embed = discord.Embed(
                title='📊 YOUR Quest Progress',
                color=discord.Color.blue()
            )
            embed.add_field(name='Quests Completed', value=str(quests_completed), inline=True)
            embed.add_field(name='Rewards Earned', value=f'{quests_completed * 100} XP', inline=True)
            embed.add_field(name='Session Status', value=f'{status_emoji} {status}', inline=False)
            embed.add_field(name='Session Duration', value=duration_str, inline=True)
            embed.add_field(name='User', value=interaction.user.mention, inline=True)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in progress: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='info', description='View global server dashboard and all active sessions')
    async def info(self, interaction: discord.Interaction):
        """View bot status, all active sessions, and server statistics."""
        await interaction.response.defer()
        try:
            # Calculate uptime
            uptime = datetime.utcnow() - self.start_time
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f'{hours}h {minutes}m {seconds}s'
            
            # Get bot ping
            ping = round(self.bot.latency * 1000)
            
            # Count active users and sessions
            active_users = len(self.active_sessions)
            total_quests_completed = sum(s.get('quests_completed', 0) for s in self.active_sessions.values())
            
            # Create dashboard embed
            embed = discord.Embed(
                title='📊 Quest Completer Global Dashboard',
                description=f'Server: {interaction.guild.name}',
                color=discord.Color.blurple()
            )
            
            embed.add_field(
                name='🤖 Bot Status',
                value=f'**Status:** 🟢 Online\n**Uptime:** {uptime_str}\n**Ping:** {ping}ms',
                inline=False
            )
            
            # Active sessions with user names
            if active_users > 0:
                active_list = '\n'.join([
                    f"• {s['username']}: {s['quests_completed']} quests ✅"
                    for s in self.active_sessions.values()
                ])
                embed.add_field(
                    name=f'👥 Active Sessions ({active_users})',
                    value=f'{active_list}\n**Total Completed:** {total_quests_completed}',
                    inline=False
                )
            else:
                embed.add_field(
                    name='👥 Active Sessions',
                    value='No active sessions',
                    inline=False
                )
            
            # User's status
            user_id = str(interaction.user.id)
            if user_id in self.active_sessions:
                session = self.active_sessions[user_id]
                user_status = f'✅ Linked & Running\n**Quests:** {session.get("quests_completed", 0)}'
            else:
                user = self.db.get_user(user_id)
                if user and user.discord_token:
                    user_status = '✅ Linked (Not Running)\nUse `/start` to begin'
                else:
                    user_status = '❌ Not Linked\nUse `/link` to get started'
            
            embed.add_field(
                name='⚙️ YOUR Account Status',
                value=user_status,
                inline=False
            )
            
            embed.set_footer(text='Quest Completer Bot | Multi-User Server Bot')
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in info: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')

async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(QuestCommands(bot))
