function gaTrack() {
$.getScript('//www.google-analytics.com/analytics.js'); // jQuery shortcut
   window.ga = window.ga || function () { (ga.q = ga.q || []).push(arguments) }; ga.l = +new Date;
   ga('create', 'UA-XXXXXXXX-X', 'auto');
 
   ga('send', 'pageview');
};