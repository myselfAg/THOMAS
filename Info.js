import '../cssPack/Info.css';

export default function Info() {
    const handleTestPy = () => {
        window.open("http://localhost:8502", "_blank");
      };
    
      const handleAppPy = () => {
        window.open("http://localhost:8503", "_blank");
    
      };
  return (
    <>
        <div className='body' >

            <div className='info'>
                <h1>THOMAS & FRIENDS</h1>
                <div>
                    <p>Train Habitation and Occupancy Monitoring with Advanced Sensors (T.H.O.M.A.S.) uses advanced sensors and AI to track real-time passenger density and coach occupancy. With live visuals, smart dashboards, and guidance displays, it ensures safer, smoother, and smartertrain journeys.</p>
                    <div className='btns'>
                        <button onClick={handleTestPy}>Software</button>
                        <button onClick={handleAppPy}>Hardware</button>
                    </div>
                </div>
            </div>

        </div>
    </>
  )
}
