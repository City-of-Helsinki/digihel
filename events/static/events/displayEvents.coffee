window.displayEvents = (eventData, grid = false) ->
  $list = $(".events-highlights, .events-index")
  $footnote = $(".events-source")
  if not grid
    eventData = eventData[..1]
  if Object.keys(eventData).length == 0
    $list.append $("<h4 class='event-title'>Tällä hetkellä ei tulevia tapahtumia.</h4>")
  for event in eventData
    eventName = event.name.fi || event.name.en
    if event.info_url?
      eventLink=event.info_url.fi || event.info_url.en
    else
      eventLink = "http://www.hel.fi/www/helsinki/fi/tapahtumakalenteri/tapahtuma/?id=" + event.id
    if event.images.length > 0
      eventImage=event.images[0].url
    else
      eventImage = "/static/images/share-default.jpg"
    if event.location?
      eventLocationLinkFi = "https://palvelukartta.hel.fi/unit/" + event.location.id.split('tprek:').pop()
      eventLocationLinkEn = "https://servicemap.hel.fi/unit/" + event.location.id.split('tprek:').pop()
      eventLocationName = event.location.name.fi || event.location.name.en
      if eventLocationName == event.location.name.fi?
        eventLocationLink = eventLocationLinkFi
      else
        eventLocationLink = eventLocationLinkEn
    else
      eventLocationLink = null
      eventLocationName = event.location_extra_info.fi || event.location_extra_info.en
    if event.short_description?
      eventDescription = event.short_description.fi || event.short_description.en
    else
      eventDescriptionFi = event.description.fi.substr(0,event.description.fi.indexOf('.')+1)
      eventDescriptionEn = event.description.en.substr(0,event.description.en.indexOf('.')+1)
      eventDescription = eventDescriptionFi || eventDescriptionEn
    eventTime = moment(event.start_time).format('dd DD.MM.YYYY HH:mm')
    if grid
      $li = $("<div class='col-sm-6 col-md-4' />")
      template = """
        <div class='event-preview'>
          <a class='link-unstyled' href="#{eventLink}"><div class='event-thumbnail' style='background-image: url("#{eventImage}")'></div></a>
          <div class="event-content">
            <div class="event-meta">
              <div class='event-meta__time'><span class='glyphicon glyphicon-time' aria-hidden='true' title='aika'></span><span class='sr-only'>aika</span> <time datetime="#{eventTime}">#{eventTime}</time></div>
              <div class='event-meta__place'><span class='glyphicon glyphicon-map-marker' aria-hidden='true' title='paikka'></span><span class='sr-only'>paikka</span> <a class='link-unstyled' href="#{eventLocationLink}">#{eventLocationName}</a></div>
            </div>
            <a class='link-unstyled' href="#{eventLink}"><h4 class='event-headline'>#{eventName}</h4></a>
            <div class='event-description'>
            #{eventDescription}
            </div>
          </div>
        </div>
      """
      $li.append $($.trim template)
      $list.append $li
    else
      $li = $("<div class='event-list__item' />")
      template = """
        <h4 class="event-title"><a href="#{eventLink}">#{eventName}</a></h4>
        <div class="event-date"><span class='glyphicon glyphicon-time' aria-hidden='true' title='aika'></span><span class='sr-only'>aika</span> <time datetime="#{eventTime}">#{eventTime}</time></div>
        <div class="event-location"><span class='glyphicon glyphicon-map-marker' aria-hidden='true' title='paikka'></span><span class='sr-only'>paikka</span> <a href="#{eventLocationLink}">#{eventLocationName}</a></div>
        <a href="#{eventLink}">Lue lisää »</a>
      """
      $li.append $($.trim template)
      $footnote.before $li
  $('.event-preview').matchHeight();
