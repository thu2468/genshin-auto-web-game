from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import sys
from io import StringIO

# https://stackoverflow.com/questions/616645/how-to-duplicate-sys-stdout-to-a-log-file
class Logger(object):
    def __init__(self):
        self.stdout = sys.stdout
        self.log = StringIO()

    def write(self, message):
        self.stdout.write(message)
        self.log.write(message+'\n')
        
    def flush(self):
        self.stdout.flush()
        self.publish()
    
    def publish(self):
        if 'DISCORD_WEBHOOK' in os.environ:
            webhook = DiscordWebhook(url = os.environ['DISCORD_WEBHOOK'])
            embed = DiscordEmbed(title='Web Game Results', description=self.log.getvalue().strip('\n'), color='03b2f8')
            webhook.add_embed(embed)
            response = webhook.execute(remove_embeds = True)

sys.stdout = Logger()
