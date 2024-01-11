import { useEffect, useState } from 'react';
import './Dashboard.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


export default function Dashboard() {
    const [showInput, setShowInput] = useState(false);
    const [showInputhist,setshowInputhist]=useState(false);
    const [input, setInput] = useState("");
    const [inputhist, setInputhist] = useState("");
    const navigate=useNavigate()

    const handleManualScanClick = () => {
        setShowInput(true);
    };

    const fetchData = async () => {
        try {
            const formData = new FormData();
            formData.append('user_input', input);

            const response = await axios.post("/manual_scrape/", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });

            navigate("/cards", { state: response.data });
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };


    const fetchDataautoscan = async () => {
        try {
            const formData = new FormData();
            formData.append('user_input', input);

            const response = await axios.post("/auto_scrape/", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });

            navigate("/cards", { state: response.data });
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const viewhistory = async () => {
        try {
            const formData = new FormData();
            formData.append('user_input',inputhist);

            const response = await axios.post("/viewhistory/", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
            });

            navigate("/history", { state: response.data });
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    
    const handleManualScanSubmit = () => {
            if (input.trim() !== "") {
                fetchData();
                setShowInput(!showInput);
            }
        };
  

    return (
        <div className='dashwrapper'>
            <div className='dashcontainer'>
            </div>
            <div className="dashglassframe">
                <h1>DARKWEB MONITORING</h1>
                <div className="dashbtn">
                    <button className='dashbtns' onClick={fetchDataautoscan}>AutoScan</button>
                    <button className='dashbtns' onClick={()=>{
                        setShowInput(false)
                        setshowInputhist(!showInputhist)
                    }}>View History</button>
                    <button className='dashbtns' onClick={()=>{
                        setshowInputhist(false)
                        setShowInput(!showInput)
                    }}>ManualScan</button>
                    { showInput && (
                        <div>
                            <input className='dashinput'
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value.toLowerCase())}
                                placeholder="Enter keyword..."
                            />
                            {input && <button onClick={handleManualScanSubmit} className='dashsubmit'>Submit</button>}
                        </div>
                    )}
                    { showInputhist && (
                        <div>
                        <input className='dashinput'
                            type="text"
                            value={inputhist}
                            onChange={(e) => setInputhist(e.target.value.toLowerCase())}
                            placeholder="Search history..."
                        />
                        {inputhist && <button onClick={viewhistory} className='dashsubmit'>View History</button>}
                    </div>
                    )}
                </div>
            </div>
        </div>
    );
}
