
function formatDate(date) {
    date = new Date(date)
    var year = date.getFullYear(),
        month = date.getMonth() + 1, // months are zero indexed
        monthFormatted = month < 10 ? "0" + month : month,
        day = date.getDate(),
        dayFormatted = day < 10 ? "0" + day : day,
        hour = date.getHours(),
        minute = date.getMinutes(),
        minuteFormatted = minute < 10 ? "0" + minute : minute;

    return dayFormatted + "-" + monthFormatted + "-" + year + " " + hour + ":" +
        minuteFormatted;
}

export { formatDate }