// similar to https://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript

const base64ToBlob = (base64, mime) => {
    mime = mime || ''
    let sliceSize = 1024
    let byteChars = window.atob(base64.replace(/^data:image\/(png|jpeg|jpg);base64,/, ''))
    let byteArrays = []

    for (let offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
        let slice = byteChars.slice(offset, offset + sliceSize);
        let byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i)
        }
        let byteArray = new Uint8Array(byteNumbers)
        byteArrays.push(byteArray)
    }

    return new Blob(byteArrays, {type: mime})
}
