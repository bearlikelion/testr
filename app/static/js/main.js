$('.ui.checkbox').checkbox();

$('.message .close').on('click', function() {
  $(this).closest('.message').transition('fade');
});

$('#modal-control.button').on('click', function(){
  modal = $(this).attr('data-modal');
  console.log('Show Modal: ' + modal)

  $('#'+modal+'.modal').modal({
    blurring: true,
    observeChanges: true,
    transition: 'scale',
    onVisible: function() {
      var $content = $(this).find('.content');
      console.log(modal)
      split = modal.split('-')

      if (split[1] == 'json') {
        $.get("/testrun/"+split[2]+"/"+split[1], function (data) {
          data = JSON.stringify(data, null, 2)
          $content.html('<pre><code type="json">'+data+'</code></pre>');
          $('pre > code').each(function() {
            hljs.highlightBlock(this);
          });
        });
      } else {
        $.get("/testrun/"+split[2]+"/"+split[1], function (data) {
          $content.html('<pre><code type="plaintext">'+data+'</code></pre>');
          $('pre > code').each(function() {
            hljs.highlightBlock(this);
          });
        });
      }
    }
  }).modal('show');
});

hljs.initHighlightingOnLoad();