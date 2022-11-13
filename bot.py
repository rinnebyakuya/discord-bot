import configparser
import discord
from discord import utils
import configfile


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        author = str(message.author.id)
        if message.content == "hoo" and message.author.id != configfile.BOT_ID:
            await message.channel.send('hoo')
        if int(author) == configfile.BOT_ID:
            return
        else:
            if config.has_option(author, "count"):
                count = int(config[author]["count"])
                count += 1
                config[author]["count"] = str(count)
                if count == 10 and message.author.id != configfile.BOT_ID:
                    member = utils.get(message.guild.members,
                                       id=message.author.id)
                    role = utils.get(message.guild.roles,
                                     id=configfile.ROLES[EMOJI_HERE])
                    await member.add_roles(role)
                    print("Granted the role YOUR_ROLE_NAME_HERE! to user {0}".format(
                        message.author.id))
            else:
                config.add_section(author)
                config.set(author, "count", "1")
            with open('users.ini', 'w') as configfile:
                config.write(configfile)

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == configfile.POST_ID:
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = utils.get(message.guild.members, id=payload.user_id)
            try:
                emoji = str(payload.emoji)
                role = utils.get(message.guild.roles,
                                 id=configfile.ROLES[emoji])
                if (len([i for i in member.roles if i.id not in configfile.EXCROLES]) <= configfile.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(
                        member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print(
                        '[ERROR] Too many roles for user {0.display_name}'.format(member))

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=configfile.ROLES[emoji])
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(
                member, role))
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=configfile.ROLES[emoji])
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(
                member, role))
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


config = configparser.ConfigParser()
config.read('users.ini', encoding="utf-8")
client = MyClient(intents=discord.Intents.all())
client.run(configfile.TOKEN)
