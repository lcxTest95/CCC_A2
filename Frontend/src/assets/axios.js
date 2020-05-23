import axios from "axios";
axios.defaults.headers = {
  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
}
axios.defaults.headers.post={
  'Content-Type' : 'application/json;charset=UTF-8'
}
axios.defaults.headers.post={
  'Access-Control-Allow-Origin' : '*'
}
// header("Access-Control-Allow-Origin", "*");
var instance = axios.create({
  timeout: 360000,
});
export default instance;