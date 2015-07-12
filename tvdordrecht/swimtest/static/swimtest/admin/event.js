var $ = django.jQuery;
// var clock = 0;

// Document ready...
$(function() {
  
  // All stopwatch fields have a default value of '00:00:00'. This
  // makes the manual input much quicker. But fails on validation of the form.
  // Thats why on submit set all fields containing '00:00:00' to empty string.
  $( "#event_form" ).submit(function( event ) {
    $("#event_form *").filter(':input').each(function(){
      if (this.value == '00:00:00') {
        this.value = '';
      }
    });
  });
  
  // Change the background color of stopwach fields on load.
  $('input[type=time].sTimeField').each(function() {
    if (this.value != '00:00:00') {
      $(this).css('background', '#dfd');
    }
  });
  
  // Change the background color of stopwach fields on change.
  $('input[type=time].sTimeField').change(function() {
    if (this.value != '00:00:00') {
      $(this).css('background', '#dfd');
    }
  });

  // // Format milliseconds to HH:MM:SS:ffff.
  // var toHHMMSSffff = function (i) {
  //     var i = parseInt(i, 10)
  //     var num = i / 1000;
  //     var hours   = Math.floor(num / 3600);
  //     var minutes = Math.floor((num - (hours * 3600)) / 60);
  //     var seconds = Math.floor(num - (hours * 3600) - (minutes * 60));
  //     var fractions = i - (hours * 3600) - (minutes * 60) - (seconds * 1000);
  //
  //     if (hours   < 10) {hours   = "0"+hours;}
  //     if (minutes < 10) {minutes = "0"+minutes;}
  //     if (seconds < 10) {seconds = "0"+seconds;}
  //     if (fractions < 10 ) {fractions = "0"+fractions;}
  //     if (fractions < 100 ) {fractions = "0"+fractions;}
  //     var time = hours+':'+minutes+':'+seconds+ '.' +fractions;
  //     return time;
  // }

  // // Stopwatch
  // var Stopwatch = function(elem, options) {
  //
  //   var timer       = createTimer(),
  //       startButton = createButton("start", start),
  //       stopButton  = createButton("stop", stop),
  //       resetButton = createButton("reset", reset),
  //       deltaButton = createButton("delta", delta),
  //       offset,
  //       clock,
  //       interval;
  //
  //   // default options
  //   options = options || {};
  //   options.delay = options.delay || 1;
  //
  //   // append elements
  //   elem.appendChild(timer);
  //   elem.appendChild(startButton);
  //   elem.appendChild(stopButton);
  //   elem.appendChild(resetButton);
  //   elem.appendChild(deltaButton);
  //
  //   // initialize
  //   reset();
  //
  //   // private functions
  //   function createTimer() {
  //     span = document.createElement("span")
  //     span.setAttribute("id", "display");
  //     return span;
  //   }
  //
  //   function createButton(action, handler) {
  //     var a = document.createElement("a");
  //     a.href = "#" + action;
  //     a.innerHTML = action;
  //     a.addEventListener("click", function(event) {
  //       handler();
  //       event.preventDefault();
  //     });
  //     return a;
  //   }
  //
  //   function start() {
  //     if (!interval) {
  //       offset   = Date.now();
  //       interval = setInterval(update, options.delay);
  //     }
  //   }
  //
  //   function stop() {
  //     if (interval) {
  //       clearInterval(interval);
  //       interval = null;
  //     }
  //   }
  //
  //   function reset() {
  //     clock = 0;
  //     render();
  //   }
  //
  //   function update() {
  //     clock = delta();
  //     render();
  //   }
  //
  //   function render() {
  //     timer.innerHTML = toHHMMSSffff(clock);
  //   }
  //
  //   function delta() {
  //     var now = Date.now(),
  //         d = now - offset;
  //     return d;
  //   }
  //
  //   // public API
  //   this.start = start;
  //   this.stop  = stop;
  //   this.reset = reset;
  //   this.delta = delta;
  // };
  //
  // // Make the Stopwatch a jQuery chainable function.
  // $.fn.stopwatch = function(options) {
  //   return this.each(function(idx, elem) {
  //     new Stopwatch(elem, options);
  //   });
  // };
  //
  // var foo = $("#content-main").stopwatch();

});

// // Format milliseconds to HH:MM:SS:ffff.
// var toHHMMSS = function (i) {
//     var i = parseInt(i, 10)
//     var num = i / 1000;
//     var hours   = Math.floor(num / 3600);
//     var minutes = Math.floor((num - (hours * 3600)) / 60);
//     var seconds = Math.floor(num - (hours * 3600) - (minutes * 60));
//     var fractions = i - (hours * 3600) - (minutes * 60) - (seconds * 1000);
//     if (fractions >= 5000) {
//       seconds += 1;
//     }
//     if (hours   < 10) {hours   = "0"+hours;}
//     if (minutes < 10) {minutes = "0"+minutes;}
//     if (seconds < 10) {seconds = "0"+seconds;}
//     var time = hours+':'+minutes+':'+seconds;
//     return time;
// }

// var StopwatchShortcuts = {
//     clockInputs: [],
//     shortCutsClass: 'now_link',
//     init: function() {
//         var inputs = document.getElementsByTagName('input');
//         for (i=0; i<inputs.length; i++) {
//             var inp = inputs[i];
//             if (inp.getAttribute('type') == 'time' && inp.className.match(/sTimeField/)) {
//                 StopwatchShortcuts.addClock(inp);
//             }
//         }
//     },
//     // Add clock widget to a given field
//     addClock: function(inp) {
//         var num = StopwatchShortcuts.clockInputs.length;
//         StopwatchShortcuts.clockInputs[num] = inp;
//         // Shortcut "Now" link
//         var shortcuts_span = document.createElement('span');
//         shortcuts_span.className = StopwatchShortcuts.shortCutsClass;
//         inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
//         var now_link = document.createElement('a');
//         now_link.setAttribute('href', "javascript:StopwatchShortcuts.setTimeToField(" + num + ");");
//         now_link.appendChild(document.createTextNode(gettext('Now')));
//         shortcuts_span.appendChild(document.createTextNode('\240'));
//         shortcuts_span.appendChild(now_link);
//     },
//
//     setTimeToField: function(num) {
//       arr = $('#display').text().split(".")
//       StopwatchShortcuts.clockInputs[num].value = arr[0];
//     }
// }
//
// addEvent(window, 'load', StopwatchShortcuts.init);
//
//
// $()
// var reinitDateTimeShortCuts = function() {
//   // Reinitialize the calendar and clock widgets by force
//   if (typeof DateTimeShortcuts != "undefined") {
//     $(".datetimeshortcuts").remove();
//     DateTimeShortcuts.init();
//   }
// };