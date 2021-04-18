start_user = (
    '<b>Olá!</b>'
    '\nEste bot é capaz de alertar as pessoas quando um chat de voz começar.'
    '\nBasta me adicionar em um grupo e começar um novo chat de voz para que as pessoas possam ligar os alertas.'
    '\n'
    '\nGrupos e canais públicos com chats de voz ligados são listados no canal @Chats_de_Voz'
    '\ne no site https://ChatsdeVoz.com'
    '\nPara que seu grupo ou canal apareça no canal e no site, basta que o bot seja adicionado neles.'
    '\n'
    '\nCaso queira utilizar o bot para fazer inserções de voz com mensagens dos ouvintes, visite:'
    '\nhttps://blog.gabrf.com/posts/TelegramVoiceChat/'
)

start_admin = (
    '<b>Encaminhamento de mensagens de voz iniciado!</b>'
    '\nTodas as mensagens enviadas ao bot chegarão aqui.'
    '\nPara encerrar o encaminhamento, finalize o chat de voz ou envie <code>/parar</code> no grupo.'
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

voice_started = (
    '<b>Chat de Voz iniciado no grupo {}</b>'
    '\n<a href="https://t.me/c/{}/{}">Clique aqui para participar!</a>'
    '\n\nPara não receber mais alertas deste grupo'
    '\n<a href="https://t.me/ChatDeVozBot?start={}">clique aqui</a>.'
)

voice_started_group = (
    '<b>@{0}</b>'
    '\n<a href="https://t.me/{0}?voicechat">Clique aqui para entrar no chat de voz</a>'
)

voice_sub = (
    'Te adicionei na lista do grupo <b>{}</b>!'
    '\nIrei te avisar assim que um novo chat de voz começar.'
    '\nQuer conhecer mais grupos? @Chats_de_Voz'
)

voice_unsub = (
    'Você não mais receberá alertas do grupo <b>{}</b>.'
    '\nQuer conhecer mais grupos? @Chats_de_Voz'
)

notified = (
    '🗣<b>{} pessoas notificadas do início do chat de voz.</b>🗣'
    '\nQuer receber um aviso também? <a href="https://t.me/ChatDeVozBot?start={}">Clique aqui</a>!'
)

not_in_group = (
    'Infelizmente não faço parte deste grupo.'
    '\nPeça para alguém que administra o grupo para me adicionar lá como administrador e assim poderei te enviar alertas quando um chat de voz começar.'
)

