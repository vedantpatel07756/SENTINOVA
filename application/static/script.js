const value = document.getElementById("value").innerHTML; // Get innerHTML of the element
console.log(value);

var arrayFromString = value.split(","); // Split the obtained string

console.log(arrayFromString); // Output the resulting array

// Pie Chart 

// Sample data for sentiment distribution pie chart
const data = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [{
      data: arrayFromString, // Example data percentages
      backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'], // Example colors
      hoverBackgroundColor: ['#36A2EB', '#FF6384', '#FFCE56']
    }]
  };
  
  // Create pie chart
  const ctx = document.getElementById('sentimentPieChart').getContext('2d');
  const sentimentPieChart = new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      responsive: false, // Set to true for responsive charts
      maintainAspectRatio: false // Set to true if you want to maintain aspect ratio
    }
  });




// Half Dougnut 

const avg=document.getElementById("avg_value").innerHTML ;
let cal_avg=parseInt(avg);
console.log(cal_avg);

var emoji=document.getElementById("emoji");



if(cal_avg>100){
  cal_avg=100;
}else{
  if(cal_avg<0){
    cal_avg=0;
  }
}

// const avg=80;
console.log("avg="+parseInt(avg));
 // Get the canvas element
 var canvas = document.getElementById('doughnutChart');
 var ct = canvas.getContext('2d');

 var color = "#36A2EB";
 var text="Positive";

 if(cal_avg<40){
  color="#FF6384";
  emoji.innerHTML="😢";
  text="Negative";
 }else{
  if(cal_avg>=40 && cal_avg<=60){
    color="#FFCE56"
    emoji.innerHTML="😞";
    text="Neutral"
  }else{
    color="#36A2EB";
    emoji.innerHTML="😍";
    text="Positive";
  }

 }
 // Define the data for the doughnut chart
 var dataD = {
   labels: [text, "Total"],
   datasets: [{
     label: 'Emotion Score',
     data: [avg, 100-avg],
     backgroundColor: [color,"#b7b6b6"]
   }]
 };

//  Define options for the doughnut chart
 var options = {
   rotation: -90,
   circumference: 180,
   aspectRatio: 3,
 };


// Create the half doughnut chart
var chart = new Chart(ct, {
  type: 'doughnut',
  data: dataD,
  options: options
});







// Rader Chart 

const raderData=document.getElementById("raderdata");
console.log("Rader data ="+ raderData.innerHTML)


// Given data string
// const dataString = "({'love': 9, 'happy': 7, 'good': 6, 'healthy': 5, 'fun': 4}, {'no': 5, 'hard': 2, 'ill': 2, 'supremacists': 1, 'tired': 1}, {'#': 285, '!': 64, '@': 61, 'user': 59, 'the': 25})";
const dataString = raderData.innerHTML
// Function to convert the data string into an array of objects
function convertDataStringToArray(dataString) {
  // Removing surrounding parentheses and splitting the string by "}, {"
  const parts = dataString.slice(2, -2).split("}, {");

  // Converting each part into an object and pushing them into an array
  const dataArray = parts.map(part => {
    // Splitting each part by comma and constructing an object from key-value pairs
    const keyValuePairs = part.split(", ");
    const obj = {};
    keyValuePairs.forEach(pair => {
      const [key, value] = pair.split(": ");
      obj[key.slice(1, -1)] = parseInt(value);
    });
    return obj;
  });

  return dataArray;
}

// Call the function to convert the data string into an array of objects
const dataArray = convertDataStringToArray(dataString);

// Output the resulting array
console.log(dataArray);

//// Given data - corrected format
const raderdata =dataArray
var bgcolor;
// Function to convert parsed data into Chart.js compatible format
function convertDataToChartFormat(dataObject, labelPrefix) {
  const labels = Object.keys(dataObject);
  const data = Object.values(dataObject);

  console.log("LabelPrefix="+labelPrefix);
  if(labelPrefix=='Negative'){
    // console.log("Contition true")
    bgcolor='rgba(255, 99, 132, 0.2)';
  }else{
    if(labelPrefix=='Neutral'){
      bgcolor='#ffcf5678';
    }else{
      bgcolor='rgba(75, 192, 192, 0.2)';
    }
    
  }
  // Sort labels by descending order of their respective data values
  const sortedLabels = labels.sort((a, b) => dataObject[b] - dataObject[a]);

  // Prepare the dataset
  const dataset = {
    labels: sortedLabels.slice(0, 5), // Considering top 5 labels
    datasets: [{
      label: labelPrefix,
      data: Object.values(dataObject).slice(0, 5), // Considering top 5 values
      backgroundColor:bgcolor,
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };

  return dataset;
}

// Convert each part of the parsed data into Chart.js compatible format
const positiveData = convertDataToChartFormat(raderdata[0], 'Positive');
const negativeData = convertDataToChartFormat(raderdata[1], 'Negative');
const neutralData = convertDataToChartFormat(raderdata[2], 'Neutral');

console.log('Positive Data:', positiveData);
console.log('Negative Data:', negativeData);
console.log('Neutral Data:', neutralData);

// const positiveData = {
//   labels: ['love', 'happy', 'positive', 'thankful', 'like'],
//   datasets: [{
//     label: 'Positive',
//     data: [1502, 918, 491, 486, 471],
//     backgroundColor: 'rgba(75, 192, 192, 0.2)',
//     borderColor: 'rgba(75, 192, 192, 1)',
//     borderWidth: 1
//   }]
// };

// const negativeData = {
//   labels: ['no', 'sad', 'hate', 'pay', 'bad'],
//   datasets: [{
//     label: 'Negative',
//     data: [438, 221, 137, 124, 108],
//     backgroundColor: 'rgba(255, 99, 132, 0.2)',
//     borderColor: 'rgba(255, 99, 132, 1)',
//     borderWidth: 1
//   }]
// };

// const neutralData = {
//   labels: ['#', '@', 'user', '!', '.'],
//   datasets: [{
//     label: 'Neutral',
//     data: [41261, 9863, 9548, 7696, 6540],
//     backgroundColor: 'rgba(54, 162, 235, 0.2)',
//     borderColor: 'rgba(54, 162, 235, 1)',
//     borderWidth: 1
//   }]
// };

// Configuration options for radar charts
const optionsR = {
  scale: {
    ticks: {
      beginAtZero: true
    }
  },
  aspectRatio: 1
};

// Render radar charts
const positiveChartCtx = document.getElementById('positiveChart').getContext('2d');
new Chart(positiveChartCtx, {
  type: 'radar',
  data: positiveData,
  options: optionsR
});

const negativeChartCtx = document.getElementById('negativeChart').getContext('2d');
new Chart(negativeChartCtx, {
  type: 'radar',
  data: negativeData,
  options: optionsR
});

const neutralChartCtx = document.getElementById('neutralChart').getContext('2d');
new Chart(neutralChartCtx, {
  type: 'radar',
  data: neutralData,
  options: optionsR
});



// BAR Chart 

const dataB=document.getElementById("bar").innerHTML;
console.log("DataB="+dataB.innerHTML);
// Remove parentheses and split the string by comma
var array = dataB.replace(/[()]/g, "").split(", ").map(Number);

console.log(array);


     // Python data obtained from Flask
     const topHashtags = {'Total Hashtags': array[0] }
     const topMentions = {'Total Mentions': array[1]};
     const averageCharCountPerTweet = array[2];

     // Extract labels and data from Python data
     const hashtagLabels = Object.keys(topHashtags);
     const hashtagData = Object.values(topHashtags);
     const mentionLabels = Object.keys(topMentions);
     const mentionData = Object.values(topMentions);
     const charCountLabel = 'Total Tweets';
     const charCountData = [averageCharCountPerTweet];
 
     // Chart configuration
     const chartConfig = {
       type: 'bar',
       data: {
         labels: [...hashtagLabels, ...mentionLabels, charCountLabel],
         datasets: [
           {
             label: 'Top Hashtags',
             data: [...hashtagData, 0, 0],
             backgroundColor: 'rgba(75, 192, 192, 0.2)',
             borderColor: 'rgba(75, 192, 192, 1)',
             borderWidth: 1,
             order: 1
           },
           {
             label: 'Top Mentions',
             data: [0, ...mentionData, 0],
             backgroundColor: 'rgba(255, 99, 132, 0.2)',
             borderColor: 'rgba(255, 99, 132, 1)',
             borderWidth: 1,
             order: 2
           },
           {
            //  type: 'line',
             label: 'Total Tweets',
             data: [0, 0, ...charCountData],
             borderColor: 'rgba(54, 162, 235, 1)',
             borderWidth: 2,
             fill: false,
            //  yAxisID: 'y-axis-2',
             order: 3
           }
         ]
       },
       options: {
        aspectRatio:3,
         scales: {
           yAxes: [
            //  {
            //    type: 'linear',
            //    display: true,
            //    position: 'left',
            //    id: 'y-axis-1',
            //   //  scaleLabel: {
            //   //    display: true,
            //   //    labelString: 'Frequency'
            //   //  }
            //  }
            //  },
            //  {
            //    type: 'linear',
            //    display: true,
            //    position: 'right',
            //    id: 'y-axis-2',
            //   //  gridLines: {
            //   //    drawOnChartArea: false
            //   //  },
            //   //  scaleLabel: {
            //   //    display: true,
            //   //    labelString: 'Character Count'
            //   //  }
            //  }
           ]
         }
       }
     };
 
     // Render mixed chart
     const mixedChartCtx = document.getElementById('mixedChart').getContext('2d');
     new Chart(mixedChartCtx, chartConfig);