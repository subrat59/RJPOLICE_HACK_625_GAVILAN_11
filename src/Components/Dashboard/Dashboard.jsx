import { useState } from "react";
import "./Dashboard.css"
import Search from '@mui/icons-material/TravelExplore';

export default function Dashboard(){
    const [isVpnConnected, setVpnConnected] = useState(false);
  const [wifiStatus, setWifiStatus] = useState('');

  const handleCheckboxChange = () => {
    setVpnConnected(!isVpnConnected);

    if (!isVpnConnected) {
      // Simulate turning on Wi-Fi
      setWifiStatus('Wi-Fi turned on');
    } else {
      // Simulate turning off Wi-Fi
      setWifiStatus('Wi-Fi turned off');
    }
  };

  const handleSearchButtonClick = () => {
    // Handle the search button click event
    console.log('Search button clicked');
  };

    
    return(
        <div className="main">
            <label className="btn1">
        <input
          type="checkbox"
          checked={isVpnConnected}
          onChange={handleCheckboxChange}
        />
        {isVpnConnected ? 'Connected' : 'Is Connected to VPN'}
      </label>        
            <input type="text" className="input" ></input>
            {isVpnConnected
            ?<div className="btnbox"><button>
                <Search style={{ color:"red",fontSize:"2rem" }}/>
                </button>
            </div>
            :<h1 style={{ color:"red"}}>Connect With VPN</h1>}
            
        </div>
    );
}