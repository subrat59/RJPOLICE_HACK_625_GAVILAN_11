import { useLocation, useNavigate } from 'react-router-dom';
import './Card.css';
import { useState } from 'react';
import axios from 'axios';


export default function Card() {
  const location = useLocation();
  const navigate=useNavigate()
  console.log(location.state);
  const items = location.state.reached_sites;

  const fetchData = async (item) => {
    try {
        const formData = new FormData();
        formData.append('link', "http://"+item);
        console.log(item)

        const response = await axios.post("/scrap/", formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
        });
        console.log(response.data)
         
        window.open(response.data.imgurls,'_blank')


    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

const fetchss = async (item) => {
  try {
      const formData = new FormData();
      formData.append('link', "http://"+item);
      console.log(item)

      const response = await axios.post("/scrapss/", formData, {
          headers: {
              'Content-Type': 'multipart/form-data'
          },
      });
      console.log(response.data)
      window.open(response.data.ssurl,'_blank')


  } catch (error) {
      console.error("Error fetching data:", error);
  }
};



const viewarchieves = async (item) => {
  try {
      const formData = new FormData();
      formData.append('link', "http://"+item);
      console.log(item)

      const response = await axios.post("/viewarchieves/", formData, {
          headers: {
              'Content-Type': 'multipart/form-data'
          },
      });
      console.log(response.data.image_links)
      navigate("/archieves", { state: response.data });
      


  } catch (error) {
      console.error("Error fetching data:", error);
  }
};


  return (
    <div>
      {items.map((item, index) => (
        <div key={index} className='cardwrapper'>
          <div className="cardcontents">
            <div>
            <h1>{location.state.user_input[index].toUpperCase().replace(/\+/g, ' ')}</h1>
            </div>
            <div className='links'>
              <div className='link'>Link: {item}</div>
              <div className='link'>IP:</div>
            </div>
            <div className='cardbtns'>
            <button className='cardbtn' onClick={()=>fetchData(item)}>Scrap Images</button>
              <button className='cardbtn' onClick={()=>fetchss(item)}>Preview</button>
              <button className='cardbtn' onClick={()=>viewarchieves(item)}>View Archieves</button>
            </div>
            {/* <div className="loadingbarout">
              <div className="loadingbar"></div>
            </div> */}
          </div>
          <div className="cardimage">
          <img src={location.state.images[index]} alt="" style={{ height:"100%",width:"100%" }} />
          </div>
        </div>
      ))}
    </div>
  );
}
