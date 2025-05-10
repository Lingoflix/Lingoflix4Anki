var videoSuggestions = Array(); // We will append the videos here
const displayedVideos =3;
lastDisplayedVideoIndex = 0;

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

function parseVideos(htmlText) {
  const parser = new DOMParser();
  const doc = parser.parseFromString(htmlText, "text/html");
  i = 0;

  console.log(`html length: ${htmlText.length}`)

  while (true) {
    //  Select video card
    const vcard = doc.querySelector(`#vcard${i+1}`);
    
    if (!vcard) break
    i++;

    // Select URL
    const rawURL = vcard.querySelector("a[href][target]").getAttribute("href");
    const url = rawURL.replace("watch?v=", "embed/").replace("&t=", "?start=");

    // Select subtitles
    subtitles = vcard.querySelector('.scroll-box').innerHTML;
    
    // CLeanup subtitles for readability
    subtitles = subtitles.replace("！", '！<br>')
    subtitles = subtitles.replace("？", '？<br>')
    subtitles = subtitles.replace("・", '・<br>')
    subtitles = subtitles.replace("。", '。<br>')

    videoSuggestions.push({
      "url": url,
      "subtitles": subtitles
    });
  }
  console.log(videoSuggestions)
  return videoSuggestions
}

function notifyUser(msg) {
  document.getElementById("response").innerText = msg;
}

function removeVideo(index) {
  const vid = document.getElementById(`video${index}cont`)
  vid.remove();
}

function buildVideoContainer(videoData, index) {
  notifyUser(`Embedding ${videoData}...`);
  console.log(`Embedding ${videoData}...`);
  container = document.createElement("div");
  container.id = `video${index}cont`
  container.style.cssText = "display:flex;flex-direction:row;align-items:center;margin:10px;"

  // Div for subtitles and button
  // captionDiv = container.
  container.innerHTML += `<div id="captionDiv"> ${videoData.subtitles} </div>`
  captionDiv = container.querySelector('div')

  // Create "Add to flashcard" button
  captionDiv.innerHTML += `<button id="addToFlashCardButton_${index}">Add to flashcard</button>`
  captionDiv.innerHTML += `<button id="removeVideo_${index}" onclick="removeVideo(${index})">Remove</button>`
  // button.onclick = () => saveVideoToNote(button.id); 
  container.appendChild(captionDiv);
  
  // Create the div for the YouTube player
  iframeId = `yt-player-${index}`
  container.innerHTML += `<div id="${iframeId}"></>`
  
  // Append the button and video player div to the container
  const videoGrid = document.querySelector(".video-grid");
  videoGrid.appendChild(container);
  
  // Store video data for later use
  const url = new URL(videoData.url);
  videoSuggestions.push(url);
  const videoId = url.pathname.split("/").pop();
  const rawStart = url.searchParams.get("start");
  const startTime = rawStart ? parseInt(rawStart.replace("s", "")) : 0;
  createVideoPlayer(iframeId, videoId, startTime);
  notifyUser(`To embed a video, click on the button !`);
}

kanji = document.getElementById("kanjiTextbox").value
notifyUser(`Search videos for ${kanji}`)

async function getVideoSuggestions() {

  if (videoSuggestions.length === 0) {

    kanji = document.getElementById("kanjiTextbox").value
    notifyUser(`Searching videos for "${kanji}" ...`);
    
    const response = await fetch("http://localhost:8766/getVideoSuggestions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ word: kanji })
    })
  if (!response.ok) {
      const text = await response.text();
      const errorMsg = `Error on getting videos: [${response.status}] ${text}`
      notifyUser(errorMsg);
      throw new Error(errorMsg); 
    }
    notifyUser(`Parsing response [${response.status}]...`);
    console.log(response)
    html = await response.text()
    const results = parseVideos(html)
    if (results.length === 0) {
      notifyUser("No videos found.");
      return;
    }
    notifyUser(`Found ${results.length} videos ...`);
  } 

    // console.log('got here')

    const start = lastDisplayedVideoIndex;
    const end = lastDisplayedVideoIndex+displayedVideos;

    for (i=start;i<end;i++) buildVideoContainer(videoSuggestions[i], i)
    // results.forEach((videoData, index) => buildVideoContainer(videoData, index));
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



function saveVideoToNote(buttonID) {
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

  fetch("http://localhost:8765/add_video", {
    method: 'POST',
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      videoUrl: html
    })
  })
  .then(response => response.text())
  .then(data => console.log("Saved:", data))
  .then((response) => processResponse(response))
  .then((data) => {
    alert(data + " " + data.error);
    //  Print the object to the console
    console.log(JSON.stringify(data) + " " + data.error);
  });
}



