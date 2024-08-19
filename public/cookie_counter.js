//// Replaced with server-side rendering
// function cookieParser(cookie) {
//     const cookie_list = cookie.split(';').map((e) => e.trim())

//     const cookies = {}

//     for (let i = 0; i < cookie_list.length; i++) {
//         key_val = cookie_list[i].split('=')
//         cookies[key_val[0]] = key_val[1]
//     }

//     return cookies
// }

// const cookies = cookieParser(document.cookie)

// const visitCounter = document.querySelector('#visit_counter')
// visitCounter.textContent = cookies.visit_count