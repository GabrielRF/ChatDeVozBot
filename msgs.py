start_user = (
    '<b>Olá!</b>'
    '\nEste bot é capaz de receber mensagens de voz de usuários para que sejam tocadas no chat de voz de maneira organizada.'
    '\nPara saber mais, visite:\nhttps://blog.gabrf.com/posts/TelegramVoiceChat/'
)

start_admin = (
    '<b>Encaminhamento de mensagens de voz iniciado!</b>'
    '\nTodas as mensagens enviadas ao bot chegarão aqui.'
    '\nPara encerrar o encaminhamento, envie <code>/parar</code> no grupo.'
)

start_group = (
    '<b>Participe do Chat de Voz!</b>'
    '\nClique no botão <code>/Participar</code> e envie uma mensagem de voz ao bot.'
    '\nApós aprovação, sua mensagem poderá ser tocada e respondida ao vivo!'
)

start_user_unstarted = (
    '⚠️ Antes de ativar o bot é necessário que fale comigo em privado ao menos uma vez. ⚠️'
)

start_bot_not_admin = (
    '⚠️ Por favor, me coloque como administrador do grupo e tente novamente. ⚠️'
)

stop_group = (
    '<b>Participações encerradas!</b>'
    '\n\nQuer conhecer mais sobre o bot? Fale comigo em privado!'
)

voice_start = (
    'Envie em uma única gravação sua mensagem de voz.'
    '\nCaso seja aprovada, esta mensagem será tocada no chat de voz.'
)

voice_forwarded = (
    '<b>Obrigado pela sua participação!</b>'
    '\nSua mensagem foi encaminhada para análise e poderá ser tocada em breve!'
    '\nPara enviar outra mensagem, clique novamente no botão no grupo.'
    '\n<a href="https://t.me/c/{}/{}">Clique aqui para voltar ao grupo</a>'
)

voice_not_forwarded = (
    '<b>Erro ⚠️</b>'
    '\nPara enviar uma mensagem é necessário que clique no botão da mensagem fixada no grupo.'
)

voice_not_started = (
    'Para iniciar o uso do bot envie <code>/iniciar</code>.'
    '\nEm caso de dúvidas, fale comigo em privado.'
)

voice_not_started_not_admin = (
    '<a href="tg://user?id={}">🗣 </a>Para mais informações, fale comigo em privado.'
)

voice_group_send = (
    '<a href="tg://user?id={}">🗣 </a><a href="https://t.me/ChatDeVozBot?start={}">Clique aqui</a> para enviar sua mensagem de voz'
)
