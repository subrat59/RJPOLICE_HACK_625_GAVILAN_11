import { useLocation } from 'react-router-dom';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import './Archieve.css'


export default function Archieve(){
    const location=useLocation()
    const links=location.state.image_links
    console.log(links)
    const scrollbyx=()=>{
        const currentScroll = window.scrollX;

    // Scroll horizontally by 100vw
    window.scrollTo({
      left: currentScroll + window.innerWidth,
      behavior: 'smooth', // Optional: Add smooth scrolling effect
    });
  };

  const scrollby_x=()=>{
    const currentScroll = window.scrollX;

// Scroll horizontally by 100vw
window.scrollTo({
  left: currentScroll - window.innerWidth,
  behavior: 'smooth', // Optional: Add smooth scrolling effect
});
};
    return(
        <div className='achievewrapper'>
            {links.map((imglink,index)=>(
            <div className='archievecontainer'>
                <img src={imglink} alt="" style={{ height:"auto",width:"auto" }} />
                <div className='timeipcard'>
                    <h4>TimeStamp:</h4><pre>  {location.state.timestamps[index]}</pre>
                </div>
            </div>
            ))}
            <ChevronLeftIcon sx={{ fontSize:150 , '&:hover': { color:"red" } }} style={{ position:"fixed",opacity:"0.3" , top:"50%",rightt:"90vw" , cursor:"pointer"}} onClick={scrollby_x}  />
            <NavigateNextIcon sx={{ fontSize:150 , '&:hover': { opacity: 0.5,color:"green"  }}} style={{ position:"fixed",opacity:"0.4" , top:"50%",left:"90vw" , cursor:"pointer"}} onClick={scrollbyx} />
        </div>
    );
}