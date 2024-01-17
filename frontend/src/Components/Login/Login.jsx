import { useNavigate } from 'react-router-dom';
import './Login.css'
import axios from 'axios';
import { useState } from 'react';


export default function Login(){
  const navigate = useNavigate();

  const [user,setuser]=useState("")
  const [pass,setpass]=useState("")
  const [checker,setchecker]=useState("no")

  const checkLogin = async () => {
    const formData = new FormData();
    formData.append('Username', user);
    formData.append('Password', pass);
  
    try {
      const isLogin = await axios.post("/login/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
      });
  
      console.log(isLogin.data);
      setchecker(isLogin.data.checker);
  
      if (isLogin.data.checker==='yes') {
        navigate('/dashboard');
      } 
      else alert("Wrong Credentials")
    } catch (error) {
      console.error("Error during login:", error);
      // Handle the error appropriately, e.g., show an error message to the user
    }
  };
  

  return(
    
    <div className='login_bg'>
      <div className='wrapper'>
      <div className='signin'>Sign-in</div>
      <div className='userandpass'>
          <div className='username'>Email or Username</div>
          <input className='input' onChange={(e)=>{setuser(e.target.value)}} type="text" />
          <div className='username'>Password</div>
          <input className='input' onChange={(e)=>{setpass(e.target.value)}} type="password" />
          <label><input type="checkbox"/>Remember Me</label>
          <div className='btn'>
          <button className='button' onClick={()=>{
            checkLogin()
          }}>Login</button>
          </div>
      </div>
    </div>
    </div>
  );
}