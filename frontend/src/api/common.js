import axios from 'axios'

export const HHTP = axios.create({
    baseURL: 'https://127.0.0.1:8000',
    headers: {
        Authorization: 'Bearer {token}'
    }
})
// const mocks = {
//     'auth': { 
//         'POST': { 
//             fun()
//         } 
//     },
//     'user/me': { 
//         'GET': { 
//             name: 'doggo', 
//             title: 'sir' 
//         } 
//     }
// }
  
function fun() {
    var token = '';
    axios
        .post('https://127.0.0.1:8000/api-token-auth/', {
            "username": "spanri",
	        "password": "nysha2161"
        })
        .then(response => {
            token = response.data.token;
            console.log(token)
        })
        .catch(error => {console.log(error);});
    console.log(token)
    return token;
}
//apiCall({url: 'auth', data: user, method: 'POST'})

const apiCall = ({url, method, ...args}) => {
    //if (method == 'POST') 
    return fun();
}

// const apiCall = ({url, method, ...args}) => new Promise((resolve, reject) => {
//     setTimeout(() => {
//         try {
//             resolve(mocks[url][method || 'GET'])
//             console.log(`Mocked '${url}' - ${method || 'GET'}`)
//             console.log('response: ', mocks[url][method || 'GET'])
//         } catch (err) {
//             reject(new Error(err))
//         }
//     }, 1000)
// })
  
export default apiCall