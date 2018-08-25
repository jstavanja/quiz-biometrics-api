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

    $('#wordInputWrapper').hide();
    $('.password_display').hide();
    $('.progress_password_text').hide();
    $('#keystroke_finish_text').show();
    $('#image-upload-inputs').show();

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

  // get the recording test settings from the central API
  axios.get('http://localhost:8000/quiz/2') // TODO: remove hardcoded number
    .then((response) => {
      word = response.data.keystroke_test_type.input_text,
      allRepetitions = response.data.keystroke_test_type.repetitions
      remainingRepetitions = allRepetitions
      keystrokeTestID = response.data.keystroke_test_type.id
      quizID = response.data.id

      wordDisplay.innerHTML = word
      repetitionDisplay.innerHTML = remainingRepetitions
    })

    window.currentUser = getUserId()

    setImageInputListener()
  
  // TODO: add check if current moodle user is registered already
  
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
    formData.append('face_image', file, file.filename)
    formData.append('quiz_id', quizID)
    formData.append('timing_matrix', JSON.stringify(convertToCSV(allData)))
    // show loader
    $('#image-upload-loader').show();
    axios.post('http://localhost:8000/student/register', formData)
      .then((res) => {

        $('#image-upload-loader').hide();
        $('#face_finish_text').show();
        $('#image-upload-inputs').hide();
      })
  })
}
