var videoSuggestions = Array(); // We will append the videos here


function processResponse(response) {
  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  } 
  if (response.status === 200) {
    return response.json();
  } else {
    throw new Error("Unexpected response status: " + response.status);
  }
}

function parseURLs(htmlText) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlText, "text/html");
  const links = [];

  for (let i = 1; i <= 3; i++) {
      //  Select video card
      const vcard = doc.querySelector(`#vcard${i}`);
      if (!vcard) return Array();

      // Select URL
      const rawURL = vcard.querySelector("a[href][target]").getAttribute("href");
      const url = rawURL.replace("watch?v=", "embed/").replace("&t=", "?start=");

      // Select subtitles
      subtitles = vcard.querySelector('.scroll-box').innerHTML;
      // subtitles = subtitles.replace(/！|？|・|。/g, '<br>')
      subtitles = subtitles.replace("！", '！<br>')
      subtitles = subtitles.replace("？", '？<br>')
      subtitles = subtitles.replace("・", '・<br>')
      subtitles = subtitles.replace("。", '。<br>')

      links.push({
        "url": url,
        "subtitles": subtitles
      });
  }
  
  console.log(links);
  return links
}

function notifyUser(msg) {
  document.getElementById("response").innerText = msg;
}

notifyUser(`Search videos for ${kanjis}`)

function getVideoSuggestions() {
  const kanji = document.getElementById("kanjiTextbox").value
  notifyUser(`Searching videos for "${kanji}" ...`);

  fetch("http://localhost:8766/getVideoSuggestions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ word: kanji })
  })
  .then(async response => {
    // if (!response.ok) {
    //   const errorMsg = `Error on getting videos: [${response.status}] ${response.text}`
    //   notifyUser(errorMsg);
    //   throw new Error(errorMsg); 
    // }
    notifyUser(`Parsing response [${response.status}]...`);
    return response.text()
  })
  // .catch(error => {
  //   document.getElementById("response").innerText = "Error: " + error;
  // })
  .then(htmlText => parseURLs(htmlText))
  .then(results => {
    if (results.length === 0) {
      // notifyUser("No videos found.");
      return;
    }
    notifyUser(`Found ${results.length} videos ...`);
    
    results.forEach((videoData, index) => {
      notifyUser(`Embedding ${videoData.url}...`);
      // Create a new div container for the video and button
      container = document.getElementById(`video${index}cont`)
      if (container === null) {
        container = document.createElement("div");
        container.id = `video${index}cont`
        container.style.cssText = "display:flex;flex-direction:row;align-items:center;margin:10px;"
      }

      // Div for subtitles and button
      // captionDiv = container.
      const captionDiv =  document.createElement("div");
      captionDiv.id = 'captionDiv';
      captionDiv.innerHTML = videoData.subtitles;

      // Create the "Add to flashcard" button
      const buttonID = `addToFlashCardButton_${index}`;
      button = document.getElementById(buttonID);
      if (button === null) {
        captionDiv.innerHTML += `<button id="${buttonID}">Add to flashcard</button>`
        // button.onclick = () => attachVideo(button.id); 
      }
        
        // Create the div for the YouTube player
        const iframeId = `yt-player-${index}`;
        playerDiv = document.getElementById(iframeId);
        if (playerDiv === null) {
          container.innerHTML += `<div id="${iframeId}"></>`
        }

        const videoGrid = document.querySelector(".video-grid");
        
        // Append the button and video player div to the container
        container.appendChild(captionDiv);
        // container.appendChild(playerDiv);
        videoGrid.appendChild(container);
        
        // Store video data for later use
        const url = new URL(videoData.url);
        videoSuggestions.push(url);
        const videoId = url.pathname.split("/").pop();
        const rawStart = url.searchParams.get("start");
        const startTime = rawStart ? parseInt(rawStart.replace("s", "")) : 0;
        createVideoPlayer(iframeId, videoId, startTime);
        notifyUser(`To embed a video, click on the button !`);

      });
    })
    .catch((err) => {
      console.error(err);
      notifyUser(`JS Error : ${err}`);
    });
}

function createVideoPlayer(iframeId, videoId, start) {
  console.log("Creating player for videoId:", videoId, "at start:", start);
  new YT.Player(iframeId, {
    videoId: videoId,
    playerVars: {
      // autoplay: 1,
      cc_load_policy: 1,
      start: start,
      // end : start + 10,
      // loop : 1,
      // playlist: videoId
    },
    events: {
      onReady: (event) => { 
        event.target.seekTo(start, true); // Why are we doing this manually ?
        event.target.pauseVideo();
      },
      onStateChange: (event) => {
        if (event.data === YT.PlayerState.PLAYING) {
          const player = event.target;
          const checkInterval = setInterval(() => {
            const currentTime = player.getCurrentTime();
            if (currentTime >= start + 10) {
              // 5 seconds after start, but do it only once
              player.pauseVideo();
              event.target.seekTo(start, true);
              clearInterval(checkInterval);
            }
          }, 5000); // check twice a second
        }
      },
    },
  });
}



function attachVideo(buttonID) {
  // Get index id from button
  const index = buttonID.split("_")[1];
  //  Check the index is a valid integer
  if (isNaN(index)) {
    console.error("Invalid index:", index);
    return;
  } else {
    console.log("Button clicked for index " + index + " and videoURL: " + videoSuggestions[index]);
    console.log(videoSuggestions);
  }
  videoURL = videoSuggestions[index]
  
  // // Get iframe element with matching id
  const iframe = document.getElementById(`yt-player-${index}`);
  if (!iframe) {
    console.error("Iframe not found for index:", index);
    return;
  }

  // Copy iframe's outer HTML
  const html = iframe.outerHTML;
  console.log("HTML to add:", html);
  // Use regex to replace "https://www.youtube.com/embed/ ... ?" with the videoURL variable
  

  // Find the flashcard id
  const card = document.getElementById("cardDetailsBox")
  const cardIdP = card.querySelector("p");
  if (!cardIdP) {
    console.error("Flashcard not found.");
    return;
  }
  
  const cardID = card.querySelector("p").textContent.replace("ID: ", "");
  console.log(`Adding video ${videoURL} to flashcard [${cardID}] back field.`);

  addVideoToCard(html)  
  .then((response) => processResponse(response))
  .then((data) => {
    alert(data + " " + data.error);
    //  Print the object to the console
    console.log(JSON.stringify(data) + " " + data.error);
  });
}



function addVideoToCard(html) {
  fetch("http://localhost:8765/add_video", {
    method: method,
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      videoUrl: html
    })
  })
  .then(response => response.text())
  .then(data => console.log("Saved:", data));

}


