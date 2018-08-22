// measurement data object, later filled and pushed to the api
let allData = {
  h: [],
  dd: [],
  ud: []
}

let previousDownKey, currentUpKey, currentDownKey, // keys needed for measurements
    wordInputWrapper, wordInput, wordDisplay, repetitionDisplay, submitUsernameButton, usernameInput, firstTimeCheckbox // DOM elements

// default settings, later pulled from api
let word = 'loading', allRepetitions = 10, remainingRepetitions

// other variables, needed for computations and checks
let currentIndexWritten = 0, hDurations = [], ddDurations = [], udDurations = [], keyTimes = {}

function getUserId() {
  let regex = /[?&]([^=#]+)=([^&#]*)/g,
        url = window.location.href,
        params = {},
        match;

    while (match = regex.exec(url)) {
        params[match[1]] = match[2];
    }

    return params.user
}

const measureTimes = (e) => {
  recordDownUpDuration(e)
}

const recordDownUpDuration = (e) => {
  const kc = e.keyCode
  if (kc === 27 || kc === 16 || kc === 17 || kc === 18 || kc === 91 || kc === 93) return // not looking at shifts, esc, alt and ctrl

  // If the key DOWN-UP pattern wasn't yet recorded, initialize empty object
  if (!keyTimes[kc]) {
    keyTimes[kc] = {}
  }

  if (e.type === 'keydown') {

    currentDownKey = { key: keyCodes[kc], timestamp: Date.now() }

    // Record key down press timestamp if key is not yet being held
    if (!e.repeat) {
      keyTimes[kc].lastDown = Date.now()
      
      recordDownDownDuration(e) // compute DOWN-DOWN duration between this and the previous keydown
      recordUpDownDuration(e) // compute UP-DOWN duration between this and the previous keyup
    }

  } else if (e.type === 'keyup') {

    // Record key up press timestamp
    keyTimes[kc].lastUp = Date.now()

    const duration = keyTimes[kc].lastUp - keyTimes[kc].lastDown
    hDurations.push({key: keyCodes[kc], duration})

    currentUpKey = { key: keyCodes[kc], timestamp: Date.now() }
    // after DOWN-UP pattern is complete, clear values for another possible measure
    keyTimes[kc] = {}
    
    checkCorrectCharacterWritten(e)
  }
}

const recordDownDownDuration = (e) => {
  if (previousDownKey) {
    ddDurations.push(
      {
        key1: previousDownKey.key,
        key2: currentDownKey.key,
        duration: Date.now() - previousDownKey.timestamp
      }
    )
  }

  previousDownKey = currentDownKey
}

const recordUpDownDuration = (e) => {
  if (currentUpKey) {
    udDurations.push(
      {
        key1: currentUpKey.key,
        key2: currentDownKey.key,
        duration: Date.now() - currentUpKey.timestamp
      }
    )
  }
}

// check if we're writing the correct letter, else restart
const checkCorrectCharacterWritten = (e) => {

  if (wordInput.value.charAt(currentIndexWritten) === word.charAt(currentIndexWritten)) {
    currentIndexWritten++
  } else {
    resetAllVariables()

    wordInput.blur()
    $('.ui.basic.modal.restart').modal('show')
    setTimeout(() => {
      wordInput.value = ''
      wordInput.focus()
      $('.ui.basic.modal.restart').modal('hide')
    }, 750)
  }
  checkIfEndOfInput(e)
}

const checkIfEndOfInput = () => {
  if (wordInput.value.length === word.length) {
    // check if everything was recorded
    if (ddDurations.length === hDurations.length-1 && udDurations.length === hDurations.length - 1) {
      remainingRepetitions--
      wordInputWrapper.classList.remove('loading')
      allData.h.push(hDurations)
      allData.dd.push(ddDurations)
      allData.ud.push(udDurations)
    } else {
      wordInput.blur()
      $('.ui.basic.modal.speed-restart').modal('show')
      setTimeout(() => {
        wordInput.value = ''
        wordInput.focus()
        $('.ui.basic.modal.speed-restart').modal('hide')
      }, 750)
    }

    resetAllVariables()
  }
  checkIfEndOfTest()
  repetitionDisplay.innerHTML = remainingRepetitions
}

const checkIfEndOfTest = () => {
  if (remainingRepetitions === 0) {
    console.log(window.currentUser)
    axios.post('http://localhost:8000/keystroke/distance', {
      "moodle_username": window.currentUser,
      "current_matrix": convertToCSV(allData),
      "test_type": keystrokeTestID
    }).then((res) => {
      console.log("server returns:")
      console.log(res.data)
      // remove 
      // check if end of whole biometrics test (two variables for each test)
    })

    document.querySelector('body').classList.add('test-complete');
  }
}

const resetAllVariables = () => {
  wordInput.value = ''
  currentIndexWritten = 0
  hDurations = []; ddDurations = []; udDurations = [];
  previousDownKey = null; currentDownKey = null; currentUpKey = null;
}

const convertToCSV = (kd) => {

  outputMatrix = []

  // loop through all sessions
  for (let sessionNumber = 0; sessionNumber < kd.h.length; sessionNumber++) {
    let holdEntrySession = kd.h[sessionNumber]
    let outputVector = []

    for (let holdNumber = 0; holdNumber < holdEntrySession.length; holdNumber++) {
      let keyPress = holdEntrySession[holdNumber]
      let nextKeyPress
      
      // add the hold duration
      outputVector.push(keyPress.duration)

      // DD and UD are of the current key and the next one (if it exists)
      if (holdNumber !== holdEntrySession.length - 1) {

        nextKeyPress = holdEntrySession[holdNumber + 1]

        outputVector.push(kd.dd[sessionNumber][holdNumber].duration)
        outputVector.push(kd.ud[sessionNumber][holdNumber].duration)
      }
    }
    outputMatrix.push(outputVector)
  }

  return outputMatrix
}

window.onload = () => {
  // get the DOM objects we need to change/record
  submitUsernameButton = document.getElementById('submitUsernameButton')
  emailInput = document.getElementById('emailInput')
  firstTimeCheckbox = document.getElementById('firstTimeCheckbox')
  wordInputWrapper = document.getElementById('wordInputWrapper')
  wordInput = document.getElementById('wordInput')
  wordDisplay = document.getElementById('wordDisplay')
  repetitionDisplay = document.getElementById('remainingRepetitions')

  $('#wordInput').on('blur', () => {
    if (remainingRepetitions === 0) return false;
    resetAllVariables()
  })

  window.addEventListener('message', (e) => {
    console.log("got message with: " + e.data)
  });

  // get the recording test settings from the central API
  axios.get('http://localhost:8000/keystroke/test/1') // TODO: remove hardcoded number
    .then((response) => {
      word = response.data.input_text,
      allRepetitions = response.data.repetitions
      remainingRepetitions = allRepetitions
      keystrokeTestID = response.data.id

      wordDisplay.innerHTML = word
      repetitionDisplay.innerHTML = remainingRepetitions
    })

    window.currentUser = getUserId()

    setImageInputListener()
  
  // TODO: add check if current moodle user is registered in our system and has a test like this registered
  // also check if he/she/it has a picture uploaded

  // bind input events to be passed into our measuring function
  wordInput.onkeydown = wordInput.onkeyup = measureTimes
}

function setImageInputListener() {
  $('#face').on('change', (e) => {
    let files = e.target.files || e.dataTransfer.files
    // TODO: add check if file is jpg or png
    if (!files.length) {
        console.log('no files')
    }
    const file = new Blob([files[0]])
    const formData = new FormData()
    formData.append('user_id', window.currentUser)
    formData.append('current_image', file, file.filename)
    axios.post('http://localhost:8000/face/distance', formData)
      .then((res) => {
        console.log("server returns:")
        console.log(res.data)
        // TODO:
        // remove input
        // check if end of biometric check
      })
  })
}
