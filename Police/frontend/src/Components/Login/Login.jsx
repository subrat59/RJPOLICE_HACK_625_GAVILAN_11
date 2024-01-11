import { useNavigate } from 'react-router-dom';
import './Login.css'


export default function Login(){

  const navigate = useNavigate();

  return(
    
    <div className='login_bg'>
      <div className='wrapper'>
      <div className='signin'>Sign-in</div>
      <div className='userandpass'>
          <div className='username'>Email or Username</div>
          <input className='input' type="text" />
          <div className='username'>Password</div>
          <input className='input' type="password" />
          <label><input type="checkbox"/>Remember Me</label>
          <div className='btn'>
          <button className='button' onClick={()=>{
            navigate('/dashboard')
          }}>Login</button>
          </div>
      </div>
    </div>
    </div>
  );
}