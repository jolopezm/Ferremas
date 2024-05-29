async function getDollarData() {
    // Get today's date in YYYY-MM-DD format
    const today = new Date();
    const formattedToday = today.toISOString().slice(0, 10);
  
    // User credentials and timeseries code (assuming these are available)
    const user = 'joselopezmignone7@gmail.com';
    const password = 'b';
    const timeseries = 'F073.TCO.PRE.Z.D'; // Assuming this is the dollar timeseries code
  
    // API URL
    const url = `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?user=${user}&pass=${password}&firstdate=${formattedToday}&lastdate=${formattedToday}&timeseries=${timeseries}&function=GetSeries`;
  
    // Make an HTTP GET request to the API
    try {
      const response = await fetch(url);
      const data = await response.json();
  
      // Extract series data from the JSON response
      const seriesData = data.Series?.Obs || [];
  
      // If data is available, return the most recent dollar rate (assuming daily data)
      if (seriesData.length > 0) {
        const latestRate = seriesData[seriesData.length - 1].VALOR;
        return latestRate;
      } else {
        console.error('No data available for the specified date');
        return null; // Return null if no data is found
      }
    } catch (error) {
      console.error('Error fetching data:', error);
      return null; // Return null in case of errors
    }
  }
  