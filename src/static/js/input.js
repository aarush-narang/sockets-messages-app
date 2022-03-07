const input = document.getElementById('input-text')
const submit = document.getElementById('input-submit')
const inputsList = document.getElementById('inputs')
const disconnect = document.getElementById('disconnect')
const connect = document.getElementById('connect')

disconnect.addEventListener('click', () => {
    socket.disconnect()
})

connect.addEventListener('click', () => {
    socket.connect()
})

submit.addEventListener('click', () => {
    const inputValue = input.value
    if (inputValue) {
        socket.emit('message', inputValue)
        input.value = ''
    }
})