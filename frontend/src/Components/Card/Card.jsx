import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Card.css';
import { useState } from 'react';
import axios from 'axios';

export default function Card() {
  const location = useLocation();
  const navigate = useNavigate();
  console.log(location.state);
  const items = location.state.reached_sites;
  const [showcards, setshowcards] = useState(false);
  const [keyword,setkeyword]=useState("")
  const [isrow,setisrow]=useState(0)

  const fetchData = async (item) => {
    setshowcards(true);
    try {
      const formData = new FormData();
      formData.append('link', "http://" + item);
      console.log(item);

      const response = await axios.post("/scrap/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);

      window.open(response.data.imgurls, '_blank');
      setshowcards(false);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fetchss = async (item) => {
    setshowcards(true);
    try {
      const formData = new FormData();
      formData.append('link', "http://" + item);
      console.log(item);

      const response = await axios.post("/scrapss/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
      window.open(response.data.ssurl, '_blank');
      setshowcards(false);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const viewarchieves = async (item) => {
    try {
      const formData = new FormData();
      formData.append('link', "http://" + item);
      console.log(item);

      const response = await axios.post("/viewarchieves/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data.image_links);
      navigate("/archieves", { state: response.data });
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  const tableCellStyle = {
    border: '1px solid aqua',
    padding: '8px',
    textAlign: 'left'
  };
  
  const tableRowStyle = {
    borderBottom: '1px solid aqua'
  };
  

 if(isrow){
  return (
    <div className='cardback'>
      {!showcards && (
        <div>
          <input className='cardsearchinput' placeholder='Search...' type="text" onChange={(e)=>{
          setkeyword(e.target.value)
          console.log(keyword)
        }} />
  
  <label class="switch">
    <input type="checkbox" onClick={()=>{
      setisrow(0)
    }}/>
    <span class="slider"></span>
  </label>
        </div>
      )}
      
      {!showcards && (
        <table className="cardtable" style={{ borderCollapse: 'collapse', width: '100%' }}>
        <thead style={{ color:"white" }}>
          <tr>
            <th style={tableCellStyle}>Site</th>
            <th style={tableCellStyle}>Link</th>
            <th style={tableCellStyle}>Relay1</th>
            <th style={tableCellStyle}>Relay2</th>
            <th style={tableCellStyle}>Relay3</th>
            <th style={tableCellStyle}>Actions</th>
          </tr>
        </thead>
        <tbody style={{ color: "white" }}>
        {items.map((item, index) => {
  // Check if the link column data contains the substring "qd"
  const containsKeyword = location.state.reached_sites[index].toUpperCase().includes(keyword.toUpperCase());

  // Render the row only if the condition is met
  if (containsKeyword) {
    return (
      <tr key={index} style={tableRowStyle}>
        <td className='tabledata' style={tableCellStyle}>
          {location.state.user_input[index].toUpperCase().replace(/\+/g, ' ')}
        </td>
        <td className='tabledata' style={tableCellStyle}>{item}</td>
        <td className='tabledata' style={tableCellStyle}>{ location.state.relays[index][0] }</td>
        <td className='tabledata' style={tableCellStyle}>{ location.state.relays[index][1] }</td>
        <td className='tabledata' style={tableCellStyle}>{ location.state.relays[index][2] }</td>
        <td className='tabledata' style={tableCellStyle}>
          <button style={{ marginBottom: "5px" }} onClick={() => fetchData(item)}>Scrap Images</button>
          <button style={{ marginBottom: "5px" }} onClick={() => fetchss(item)}>Preview</button>
          <button style={{ marginBottom: "5px" }} onClick={() => viewarchieves(item)}>View Archives</button>
        </td>
      </tr>
    );
  }

  // Return null for rows that don't meet the condition
  return null;
})}

</tbody>

      </table>      
      )}
      {showcards && <div className="cardloader"></div>}
    </div>
  );
 }
 else{
  return (
    <div>
      
      {!showcards && (
        <div>
          <input className='cardsearchinput' placeholder='Search...' type="text" onChange={(e)=>{
          setkeyword(e.target.value)
          console.log(keyword)
        }} />
  
  <label class="switch">
    <input type="checkbox" onClick={()=>{
      setisrow(1)
    }}/>
    <span class="slider"></span>
  </label>
        </div>
      )}
      {!showcards &&
      items
        .filter((item, index) =>
          location.state.reached_sites[index].toUpperCase().includes(keyword.toUpperCase())
        )
        .map((item, index) => (
          <div key={index} className='cardwrapper'>
            <div className="cardcontents">
              <div>
                <h1>{location.state.user_input[index].toUpperCase().replace(/\+/g, ' ')}</h1>
              </div>
              <div className='links'>
                <div className='link'>Link: {item}</div>
                <div className='link'>Relay1: <pre> { location.state.relays[index][0] }</pre> </div>
                <div className='link'>Relay2: <pre> { location.state.relays[index][1] }</pre> </div>
                <div className='link'>Relay3: <pre> { location.state.relays[index][2] }</pre> </div>
              </div>
              <div className='cardbtns'>
                <button className='cardbtn' onClick={() => fetchData(item)}>Scrap Images</button>
                <button className='cardbtn' onClick={() => fetchss(item)}>Preview</button>
                <button className='cardbtn' onClick={() => viewarchieves(item)}>View Archives</button>
              </div>
              {/* Add your loading bar here if needed */}
            </div>
            <div className="cardimage">
              <img src={location.state.images[index]} alt="" style={{ height:"100%",width:"100%" }} />
            </div>
          </div>
        ))
    }
      {showcards && <div class="cardloader"></div> }
    </div>
  );
  }
}
