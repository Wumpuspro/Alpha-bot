import discord
import DiscordUtils
from discord.ext import commands
import asyncio
import aiosqlite
from datetime import datetime
import aiofiles
from main1 import get_join_channels


class invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        setup = bot.loop.create_task(self.setup())
        self.tracker = DiscordUtils.InviteTracker(bot)
        self.bot.welcome_channels = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print('Invite Tracker Ready')
        await self.tracker.cache_invites()



    async def update_totals(self, member):
        invites = await member.guild.invites()

        c = datetime.today().strftime("%Y-%m-%d").split("-")
        c_y = int(c[0])
        c_m = int(c[1])
        c_d = int(c[2])

        async with self.bot.db.execute("SELECT id, uses FROM invites WHERE guild_id = ?", (member.guild.id,)) as cursor: 
            async for invite_id, old_uses in cursor:
                for invite in invites:
                    if invite.id == invite_id and invite.uses - old_uses > 0: 
                        if not (c_y == member.created_at.year and c_m == member.created_at.month and c_d - member.created_at.day < 7): 
                            print(invite.id)
                            await self.bot.db.execute("UPDATE invites SET uses = uses + 1 WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
                            await self.bot.db.execute("INSERT OR IGNORE INTO joined (guild_id, inviter_id, joiner_id) VALUES (?,?,?)", (invite.guild.id, invite.inviter.id, member.id))
                            await self.bot.db.execute("UPDATE totals SET normal = normal + 1 WHERE guild_id = ? AND inviter_id = ?", (invite.guild.id, invite.inviter.id))

                        else:
                            await self.bot.db.execute("UPDATE totals SET normal = normal + 1, fake = fake + 1 WHERE guild_id = ? and inviter_id = ?", (invite.guild.id, invite.inviter.id))

                        return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_totals(member)
        await self.bot.db.commit()
        inviter = await self.tracker.fetch_inviter(member)
        cur = await self.bot.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter.id))
        res = await cur.fetchone()
        if res is None:
            normal, left, fake = 0, 0, 0
        else:
            normal, left, fake = res
        
        total = normal - (left + fake)
        servers = get_join_channels()
        for i in servers:
            if i[1] == member.guild.id:
              try:
                channel = self.bot.get_channel(i[2])
                embed = discord.Embed(title=f'Welcome To {member.guild.name}!', description=f'**{member.mention} Was Invited By {inviter.mention}!**\n**{inviter.name}#{inviter.discriminator}** Now Has ``{total} Invites``', timestamp=datetime.now())
                embed.set_footer(text = f'Invited By {inviter.name}', icon_url=member.avatar_url)
                await channel.send(f'{member.mention}', embed=embed)
              except:
                pass



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cur = await self.bot.db.execute("SELECT inviter_id FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
        res = await cur.fetchone()
        if res is None:
            return

        inviter_id = res[0]

        await self.bot.db.execute("DELETE FROM joined WHERE guild_id = ? AND joiner_id = ?", (member.guild.id, member.id))
        await self.bot.db.execute("DELETE FROM totals WHERE guild_id = ? and inviter_id = ?", (member.guild.id, member.id))
        await self.bot.db.execute("UPDATE totals SET left = left + 1 WHERE guild_id = ? AND inviter_id = ?", (member.guild.id, inviter_id))
        await self.bot.db.commit()


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.bot.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (invite.guild.id, invite.inviter.id, invite.uses, 0, 0))
        await self.bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))

        await self.bot.db.commit()

        await self.tracker.update_invite_cache(invite)


    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.bot.db.execute("DELETE FROM invites WHERE guild_id = ? AND id = ?", (invite.guild.id, invite.id))
        await self.bot.db.commit()

        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for invite in await guild.invites():
            await self.bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
        await self.bot.db.commit()

        await self.tracker.update_guild_cache(guild)


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.db.execute("DELETE FROM totals WHERE guild_id = ?", (guild.id,))
        await self.bot.db.execute("DELETE FROM invites WHERE guild_id = ?", (guild.id,))
        await self.bot.db.execute("DELETE FROM joined WHERE guild_id = ?", (guild.id,))

        await self.bot.db.commit()

        await self.tracker.remove_guild_cache(guild)

    @commands.command()
    async def invites(self, ctx, member: discord.Member=None):
        if member is None: member = ctx.author
        cur = await self.bot.db.execute("SELECT normal, left, fake FROM totals WHERE guild_id = ? AND inviter_id = ?", (ctx.guild.id, member.id))
        res = await cur.fetchone()
        if res is None:
            normal, left, fake = 0, 0, 0
        else:
            normal, left, fake = res

        total = normal - (left + fake)

        embed = discord.Embed(title = f'Invites For {member.name}#{member.discriminator}', description=f'{member.mention} Currently Has **{total}** Invites (**{normal}** Normal, **{left}** Leaves, **{fake}** Fakes)', timestamp = datetime.now(), color = ctx.author.color)
        embed.set_footer(text = f'Requested By {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['clearinvites', 'resetinvites', 'resetinvitesall'])
    @commands.has_permissions(administrator=True)
    async def resetall(self, ctx):
        await self.bot.db.execute("UPDATE totals SET normal = 0, left = 0, fake = 0 WHERE guild_id = ?", (ctx.guild.id,))

        await self.bot.db.commit()

        embed = discord.Embed(title=f'Alpha Invite Logger', description=f'I Have Successfully Reset The Guild\'s Invites!', timestamp = datetime.now(), color = ctx.author.color)
        embed.set_footer(text = f'Requested By {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(f'{ctx.author.mention}', embed=embed)

    @resetall.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            author = ctx.message.author
            pfp = author.avatar_url
            embed = discord.Embed(title=f'Invite System Error', description='You Are Missing Required Permissions\n``Required Permissions: Administrator``', timestamp = datetime.now())
            embed.set_footer(text=f'{ctx.author.name}', icon_url=pfp)
            await ctx.send(embed = embed)



    @commands.command(aliases=['lb_inv', 'lb_invites', 'lbinv', 'top'])
    async def leaderboard_invites(self, ctx):
        buttons = {}
        for i in range(1, 6):
            buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i 

        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10
        
        
        embed = discord.Embed(title=f"Leaderboard Page {current}", description="", colour=discord.Colour.gold())
        msg = await ctx.send(embed=embed)
        
        for button in buttons:
            await asyncio.sleep(0.65)
            await msg.add_reaction(button)
            

        while True:
            if current != previous_page:
                embed.title = f'Invite Leaderboard Page {current}'
                embed.description = ""

                async with self.bot.db.execute("SELECT inviter_id, normal, left, fake FROM totals WHERE guild_id = ? ORDER BY normal - (left + fake) DESC LIMIT ? OFFSET ? ", (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as cursor:
                    index = entries_per_page*(current-1)

                    async for entry in cursor:
                        index += 1
                        inviter_id, normal, left, fake = entry
                        inviter = ctx.guild.get_member(inviter_id)
                        total = normal - (left + fake)
                        embed.description += f'``{index}.`` <@{inviter_id}> : **{total}** Invites (**{normal}** Normal , **{left}** Leaves, **{fake}** Fakes)\n'
                        embed.set_footer(text = f'Requested By {ctx.author.name}', icon_url=ctx.author.avatar_url)
                        embed.timestamp = datetime.now()
                    
                    await msg.edit(embed=embed)

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=30.0)
            
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            else:
                previous_page = current
                await msg.remove_reaction(reaction.emoji, ctx.author)
                current = buttons[reaction.emoji]



    async def setup(self):
        await self.bot.wait_until_ready()
        self.bot.db = await aiosqlite.connect("inviteData.db")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS totals (guild_id int, inviter_id int, normal int, left int, fake int, PRIMARY KEY (guild_id, inviter_id))")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS invites (guild_id int, id string, uses int, PRIMARY KEY (guild_id, id))")
        await self.bot.db.execute("CREATE TABLE IF NOT EXISTS joined (guild_id int, inviter_id int, joiner_id int, PRIMARY KEY (guild_id, inviter_id, joiner_id))")
    

        for guild in self.bot.guilds:
            for invite in await guild.invites():
                await self.bot.db.execute("INSERT OR IGNORE INTO invites (guild_id, id, uses) VALUES (?,?,?)", (invite.guild.id, invite.id, invite.uses))
                await self.bot.db.execute("INSERT OR IGNORE INTO totals (guild_id, inviter_id, normal, left, fake) VALUES (?,?,?,?,?)", (guild.id, invite.inviter.id, 0, 0, 0))
                                 
        await self.bot.db.commit()





        


def setup(client):
    client.add_cog(invites(client))