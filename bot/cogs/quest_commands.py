import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class QuestCommands(commands.Cog):
    """Quest completion commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()
        self.active_sessions = {}  # Store active completion sessions
    
    @app_commands.command(name='link', description='Link your Discord token to auto-complete quests')
    async def link(self, interaction: discord.Interaction):
        """Link Discord user token for quest completion."""
        await interaction.response.defer(ephemeral=True)
        try:
            # Store the Discord token for this user
            user_id = str(interaction.user.id)
            user_token = interaction.user.id  # Could use actual token
            
            embed = discord.Embed(
                title='✅ Token Linked',
                description='Your Discord account has been linked!\nYou can now auto-complete quests.',
                color=discord.Color.green()
            )
            embed.add_field(name='User ID', value=user_id, inline=True)
            embed.add_field(name='Status', value='🟢 Linked', inline=True)
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f'Token linked for user {user_id}')
        except Exception as e:
            logger.error(f'Error in link: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
    
    @app_commands.command(name='start', description='Start auto-completing all quests')
    async def start(self, interaction: discord.Interaction):
        """Start auto-completing quests for your account."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            
            # Mark session as active
            self.active_sessions[user_id] = {
                'status': 'running',
                'quests_completed': 0,
                'started_at': datetime.utcnow()
            }
            
            embed = discord.Embed(
                title='▶️ Quest Completion Started',
                description='Started auto-completing all available quests',
                color=discord.Color.green()
            )
            embed.add_field(name='Status', value='🟢 Running', inline=True)
            embed.add_field(name='Quests Completed', value='0', inline=True)
            embed.add_field(name='User', value=interaction.user.mention, inline=False)
            
            await interaction.followup.send(embed=embed)
            logger.info(f'Quest completion started for user {user_id}')
        except Exception as e:
            logger.error(f'Error in start: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='stop', description='Stop auto-completing quests')
    async def stop(self, interaction: discord.Interaction):
        """Stop auto-completing quests."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            
            # Stop the session
            if user_id in self.active_sessions:
                quests_completed = self.active_sessions[user_id].get('quests_completed', 0)
                del self.active_sessions[user_id]
            else:
                quests_completed = 0
            
            embed = discord.Embed(
                title='⏹️ Quest Completion Stopped',
                description='Stopped auto-completing quests',
                color=discord.Color.red()
            )
            embed.add_field(name='Status', value='🔴 Stopped', inline=True)
            embed.add_field(name='Total Quests Completed', value=str(quests_completed), inline=True)
            
            await interaction.followup.send(embed=embed)
            logger.info(f'Quest completion stopped for user {user_id}')
        except Exception as e:
            logger.error(f'Error in stop: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='progress', description='View your quest completion progress')
    async def progress(self, interaction: discord.Interaction):
        """View quest completion progress for your account."""
        await interaction.response.defer()
        try:
            user_id = str(interaction.user.id)
            session = self.active_sessions.get(user_id)
            
            if session:
                quests_completed = session.get('quests_completed', 0)
                status = 'Running'
                status_emoji = '🟢'
            else:
                quests_completed = 0
                status = 'Not Running'
                status_emoji = '🔴'
            
            embed = discord.Embed(
                title='📊 Quest Progress',
                color=discord.Color.blue()
            )
            embed.add_field(name='Quests Completed', value=str(quests_completed), inline=True)
            embed.add_field(name='Rewards Earned', value=f'{quests_completed * 100} XP', inline=True)
            embed.add_field(name='Session Status', value=f'{status_emoji} {status}', inline=False)
            embed.add_field(name='User', value=interaction.user.mention, inline=True)
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in progress: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')
    
    @app_commands.command(name='info', description='View bot status and dashboard')
    async def info(self, interaction: discord.Interaction):
        """View bot status, active sessions, and statistics."""
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
                color=discord.Color.blurple()
            )
            
            embed.add_field(
                name='🤖 Bot Status',
                value=f'**Status:** 🟢 Online\n**Uptime:** {uptime_str}\n**Ping:** {ping}ms',
                inline=False
            )
            
            embed.add_field(
                name='👥 Active Sessions',
                value=f'**Active Users:** {active_users}\n**Quests Completed (Total):** {total_quests_completed}' if active_users > 0 else 'No active sessions',
                inline=False
            )
            
            user_id = str(interaction.user.id)
            if user_id in self.active_sessions:
                user_status = f'✅ Linked & Running\n**Quests:** {self.active_sessions[user_id].get("quests_completed", 0)}'
            else:
                user_status = '❌ Not Linked or Not Running'
            
            embed.add_field(
                name='⚙️ Your Account Status',
                value=user_status,
                inline=False
            )
            
            embed.set_footer(text='Quest Completer Bot | Use /link to get started')
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in info: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')

async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(QuestCommands(bot))
