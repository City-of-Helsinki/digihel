window.displayEvents = (eventData, grid = false) ->
  $list = $(".events-highlights, .events-index")
  $footnote = $(".events-source")
  if not grid
    eventData = eventData[..2]
  if Object.keys(eventData).length == 0
    $list.append $("<h4 class='event-title'>Tällä hetkellä ei tulevia tapahtumia.</h4>")
  for event in eventData
    if event.info_url?
      eventLink=event.info_url.fi
    else
      eventLink = "http://www.hel.fi/www/helsinki/fi/tapahtumakalenteri/tapahtuma/?id=" + event.id
    if event.images.length > 0
      eventImage=event.images[0].url
    else
      eventImage = "/static/images/share-default.jpg"
    if event.location?
      eventLocationLink = "https://palvelukartta.hel.fi/unit/" + event.location.id.split('tprek:').pop()
      eventLocationName = event.location.name.fi
    else
      eventLocationLink = null
      eventLocationName = event.location_extra_info.fi
    if event.short_description?
      eventDescription = event.short_description.fi
    else
      eventDescription = event.description.fi.substr(0,event.description.fi.indexOf('.')+1)
    eventTime = moment(event.start_time).format('dd DD.MM.YYYY HH:mm')
    if grid
      $li = $("<div class='col-sm-6 col-md-4' />")
      template = """
        <div class='event-preview'>
          <a class='link-unstyled' href="#{eventLink}"><div class='event-thumbnail' style='background-image: url("#{eventImage}")'></div></a>
          <div class="event-meta">
            <span class='event-meta__time'><time datetime="#{eventTime}">#{eventTime}</time></span>
            <span class='event-meta__place'><a href="#{eventLocationLink}">#{eventLocationName}</a></span>
          </div>
          <a class='link-unstyled' href="#{eventLink}"><h4 class='event-headline'>#{event.name.fi}</h4></a>
          <div class='event-description'>
          #{eventDescription}
          </div>
        </div>
      """
      $li.append $($.trim template)
      $list.append $li
      $('.event-preview').matchHeight();
    else
      $li = $("<div class='event-list__item' />")
      template = """
        <h4 class="event-title">#{event.name.fi}</h4>
        <div class="event-date"><time datetime="#{eventTime}">#{eventTime}</time></div>
        <div class="event-location"><a href="#{eventLocationLink}">#{eventLocationName}</a></div>
        <a href="#{eventLink}">Lue lisää »</a>
      """
      $li.append $($.trim template)
      $footnote.before $li