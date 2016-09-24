function gaTrack() {
$.getScript('//www.google-analytics.com/analytics.js'); // jQuery shortcut
   window.ga = window.ga || function () { (ga.q = ga.q || []).push(arguments) }; ga.l = +new Date;
   ga('create', 'UA-83133153-1', 'auto');
 
   ga('send', 'pageview');
};