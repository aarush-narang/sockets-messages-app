const connect = document.getElementById('connect')
const disconnect = document.getElementById('disconnect')

const msgInput = document.getElementById('input-text')
const msgSubmit = document.getElementById('input-submit')
const userInput = document.getElementById('input-user')
const userSubmit = document.getElementById('user-submit')

const inputsList = document.getElementById('inputs-list')



// connect and disconnect
const socket = io.connect('https://' + window.location.hostname + ':5000');
socket.on('connect', function(msg) {
    if(!msg) return
    const msgs = msg.msgs
    const users = msg.users

    for (let i = 0; i < msgs.length; i++) {
        const msg = msgs[i]
        const user = users[i]
        const li = document.createElement('li')
        li.innerHTML = `${user}: ${msg}`
        inputsList.appendChild(li)
    }
})

if (window.closed) {
    socket.disconnect()
}


userSubmit.addEventListener('click', () => {
    if(userInput.value.length < 1) return
    if(userInput.value.length > 20) return alert('Username must be less than 20 characters')
    userInput.style.cursor = 'not-allowed'
    userSubmit.style.cursor = 'not-allowed'
    userInput.toggleAttribute('disabled', true)

    msgInput.style.cursor = 'auto'
    msgSubmit.style.cursor = 'auto'
    msgInput.toggleAttribute('disabled', false)
    msgInput.focus()
    return
})
// send message to server
msgSubmit.addEventListener('click', () => {
    if (!userInput.value || userInput.style.cursor !== 'not-allowed') {
        msgInput.style.cursor = 'not-allowed'
        msgSubmit.style.cursor = 'not-allowed'
        msgInput.toggleAttribute('disabled', true)
        return
    }
    if (msgInput.value.length > 2000) return alert('Message must be less than 2000 characters')
    
    const inputValue = msgInput.value
    if (inputValue) {
        socket.emit('user_message', inputValue, userInput.value, '0.0.0.0')
        msgInput.value = ''
    }
    msgInput.focus()
})

// recieve message from server
socket.on('user_message', (message) => {
    const li = document.createElement('li')
    li.innerHTML = `${message.user}: ${message.msg}`
    inputsList.appendChild(li)
})