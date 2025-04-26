import Cookies from "universal-cookie"

const cookies = new Cookies()

export async function userRequest(url: string, obj: {[key: string]: string | {[key: string]: string}}) {
  obj.headers = {
    'Accept': "application/json",
    'Content-Type': "application/json"
  }
  const token = cookies.get('token')

  if (token) {
    obj.headers.Authorization = 'Bearer: ' + token
  }

  if (obj.body) {
    obj.body = JSON.stringify(obj.body)
  }

  const res =  await fetch(`http://localhost:5000${url}`, obj)
  const data = await res.json()

  if (data.error && data.error == 'No token or invalid token was provided.') {
    cookies.remove('token')
  }

  return data
}

export function setUserInfo(object: {[key: string]: string}, target: string, val: string) {
  object[target] = val
}
