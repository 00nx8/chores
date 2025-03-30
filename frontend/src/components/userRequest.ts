import { Cookies } from "quasar"

export async function userRequest(url: string, obj: {[key: string]: string | {[key: string]: string}}) {
  obj.headers = {
    'Accept': "application/json",
    'Content-Type': "application/json"
  }
  const token = Cookies.get('token')

  if (token) {
    obj.headers.Authorization = 'Bearer: ' + token
  }

  const res =  await fetch(`http://localhost:5000${url}`, obj)
  const data = await res.json()
  return data
}

