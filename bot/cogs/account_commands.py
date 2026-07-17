import discord
from discord import app_commands
from discord.ext import commands
import logging
from datetime import datetime, timedelta
import psutil
import os

logger = logging.getLogger(__name__)

class AccountCommands(commands.Cog):
    """Account linking and management commands."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow()
    
    @app_commands.command(name='link', description='Link a game account')
    @app_commands.describe(
        platform='Platform name (e.g., primex)',
        username='Your account username',
        token='Your authentication token'
    )
    async def link(self, interaction: discord.Interaction, platform: str, username: str, token: str):
        """Link a game account to your Discord account."""
        await interaction.response.defer(ephemeral=True)
        try:
            embed = discord.Embed(
                title='✅ Account Linked',
                description=f'Successfully linked **{username}** on **{platform}**',
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f'Error in link: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
    
    @app_commands.command(name='unlink', description='Unlink a game account')
    @app_commands.describe(platform='Platform name (e.g., primex)')
    async def unlink(self, interaction: discord.Interaction, platform: str):
        """Unlink a game account from your Discord account."""
        await interaction.response.defer(ephemeral=True)
        try:
            embed = discord.Embed(
                title='🔌 Account Unlinked',
                description=f'Successfully unlinked your **{platform}** account',
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f'Error in unlink: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}', ephemeral=True)
    
    @app_commands.command(name='info', description='View bot status and account info')
    async def info(self, interaction: discord.Interaction):
        """View bot status and account information (Quest Completer Global Dashboard)."""
        await interaction.response.defer()
        try:
            # Calculate uptime
            uptime = datetime.utcnow() - self.start_time
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f'{hours}h {minutes}m {seconds}s'
            
            # Get bot ping
            ping = round(self.bot.latency * 1000)
            
            # Create main dashboard embed
            embed = discord.Embed(
                title='📊 Quest Completer Global Dashboard',
                color=discord.Color.blurple()
            )
            
            # Bot Status section
            embed.add_field(
                name='🤖 Bot Status',
                value=f'**Status:** 🟢 Online\n**Uptime:** {uptime_str}\n**Ping:** {ping}ms',
                inline=False
            )
            
            # Active Sessions section
            embed.add_field(
                name='👥 Active Sessions',
                value='No active sessions',
                inline=False
            )
            
            # Your Account Status section
            embed.add_field(
                name='🔐 Your Account Status',
                value='**Token Linked:** ❌ Not Linked\n**Running Completer:** No',
                inline=False
            )
            
            embed.set_footer(text='Quest Completer Bot | Made by Siddharth')
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            logger.error(f'Error in info: {e}')
            await interaction.followup.send(f'❌ Error: {str(e)}')

async def setup(bot):
    """Setup the cog."""
    await bot.add_cog(AccountCommands(bot))
