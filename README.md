# genshin-auto-web-game
Play the current Genshin Impact web game automatically using workflow actions, currently only works on global (EN) server. __Use at your own risk.__

Current Game: `Hilidream Camp`
## Setup
1. Fork this repo and perform the following on your local fork.
2. Navigate to [https://genshin.mihoyo.com/en/home](https://genshin.mihoyo.com/en/home), open the javascript console `ctrl+shift+j` and run the following code: `copy(document.cookie)`
3. Create a new repo secret (`Settings` > `Secrets`) and name it `COOKIE`, then paste the value you copied in step 2 into the value field.
4. Navigate to the `Actions` tab and run the `Web Game` workflow.

### Optional
1. If you want to get results via a discord webhook you can add another secret named `DISCORD_WEBHOOK` which contains your webhook URL.