css = """
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 10%;
}
.chat-message .avatar img {
    max-width: 72px;
    max-height: 72px;
    border-radius: 40%;
    object-fit: cover;
}
.chat-message .message {
    width: 75%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="bot.jpg" alt="Bot" width="40" height="40">
    </div>
    <div class="message">$MSG</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="user.jpg" alt="User" width="40" height="40">
    </div>
    <div class="message">$MSG</div>
</div>
"""
