import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';


export default function HistoryCard() {
  const location = useLocation();
  const navigate=useNavigate()
  console.log(location.state);
  const items = location.state.links;

 


const viewarchieves = async (item) => {
  try {
      const formData = new FormData();
      formData.append('link', item);
      console.log(item)

      const response = await axios.post("/viewarchieves/", formData, {
          headers: {
              'Content-Type': 'multipart/form-data'
          },
      });
      console.log(response.data)
      navigate("/archieves", { state: response.data });
      


  } catch (error) {
      console.error("Error fetching data:", error);
  }
};


  return (
    <div>
      {items.map((item, index) => (
        <div key={index} className='cardwrapper' style={{height:"230px"}}>
          <div className="cardcontents" style={{ width:"100%",height:"100%"}}>
            <div>
            <h1>{location.state.user_input.toUpperCase().replace(/\+/g, ' ')}</h1>
            </div>
            <div className='links'>
              <div className='link'>Link: {item}</div>
            </div>
            <div className='cardbtns'>
              <button className='cardbtn' onClick={()=>viewarchieves(item)}>View Archieves</button>
            </div>
            {/* <div className="loadingbarout">
              <div className="loadingbar"></div>
            </div> */}
          </div>
        </div>
      ))}
    </div>
  );
}
