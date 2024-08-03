(function($) {

    $.widget("tas.talitaPlayer", {

        options: {

        },

        _destroy: function() {

            // Remove Window events
            $(window).off("scroll.talitaPlayer");

            // Remove Drag and Drop events
            this.element.off("mousedown");

            // Remove Interception events
            $(this.options.track).off("click");
            $(this.options.track).off("mouseover");
            $(this.options.track).off("mouseleave");

            // Clear marks on text
            let clicked = $(".talita-text-clicked");

            if (clicked)
                clicked.removeClass("talita-text-clicked");
            
            // Remove Container's Inner Elements
            this.element.text("");
            // Remove Styles
            this.element.removeClass("started");
            // Remove Width and Height
            this.element.removeAttr("style");

        },

        _create: function() {
            
            this._createInterface();

            this._dragAndDropEvent();
            
            this._closeEvent();

            this._resizeEvent();
            
            this._interceptClickEvent();

            this._scrollEvent();
                        
        },

        _createInterface: function() {

            let component = this.element;

            component.width(this.options.width);
            component.height(this.options.height);

            component.addClass("started");
            component.addClass("background");

            if (!this.options.position || this.options.position == "right")
                component.addClass("right");

            if (this.options.position == "left")
                component.addClass("left");

            let closeButton = $("<div>");

            closeButton.attr("id", "close-button");

            component.append(closeButton);

            let video = $("<video>");

            video.attr("id", "talita-player");

            component.append(video);

            let resizeButton = $("<div>");

            resizeButton.attr("id", "resize-button");

            component.append(resizeButton);

        },

        _scrollEvent: function() {

            let component = this.element;

            let iniScrollTop = 0;
            let iniScrollLeft = 0;

            $(window).bind("scroll.talitaPlayer", function() {

                let curScrollTop = $(this).scrollTop();
                let curScrollLeft = $(this).scrollLeft();

                let componentTop = component.offset().top;
                let componentLeft = component.offset().left;

                let newComponentTop = componentTop + (curScrollTop - iniScrollTop);
                let newComponentLeft = componentLeft + (curScrollLeft - iniScrollLeft);

                component.offset({
                    top: newComponentTop,
                    left: newComponentLeft
                });

                iniScrollTop = curScrollTop;
                iniScrollLeft = curScrollLeft;

            });

            $(window).trigger("scroll.talitaPlayer");

        },

        _interceptClickEvent: function() {

            let component = this.element;

            let videoPath = this.options.videoPath;
            let videoId = this.options.videoId;
            let track = this.options.track;

            if (!videoPath)
            {
                console.error("You must provide a videoPath");
                return;
            }

            if (!videoId)
            {
                console.error("You must provide a videoId");
                return;
            }

            if (!track)
            {
                console.error("You must provide a track");
                return;
            }

            $(track).mouseover(function(event) {

                let element = $(this);

                if (element.is("img") || element.is("area"))
                    element.addClass("talita-image-over");
                else
                    element.addClass("talita-text-over");

            });

            $(track).mouseleave(function(event) {

                let element = $(this);

                if (element.is("img") || element.is("area"))
                    element.addClass("talita-image-over");
                else
                    element.removeClass("talita-text-over");

            });

            $(track).click(function(event) {
                
                event.preventDefault();

                // Remove background image
                component.removeClass("background");

                // Apply style when clicked
                let element = $(this);

                if (!element.is("img") && !element.is("area"))
                {
                    let clicked = $(".talita-text-clicked");

                    if (clicked)
                        clicked.removeClass("talita-text-clicked");
    
                    $(this).addClass("talita-text-clicked");
                }

                // Loads video on video tag
                let video = $(this).attr(videoId);
                
                let player = component.find("video")
                                      .get(0);

                player.src = videoPath + video;
                player.load();
                player.play();
                
            });

        },

        _resizeEvent: function() {

            let container = this.element;
            let resizeButton = $("div#resize-button");

            let currentX = 0;
            let currentY = 0;

            let stopResize = (event) => {

                event.stopPropagation();
                event.preventDefault();

                let viewport = $(window);

                viewport.off("mousemove");
                viewport.off("mouseup");

            };

            let resize = (event) => {

                event.stopPropagation();
                event.preventDefault();

                let newWidth = 0;
                let newHeight = 0;

                let currentWidth = container.width();
                let currentHeight = container.height();

                let offsetX = event.pageX - currentX;
                let offsetY = event.pageY - currentY;

                if (Math.abs(offsetX) > Math.abs(offsetY))
                {
                    newWidth = currentWidth + offsetX;
                    newHeight = newWidth * (currentHeight / currentWidth);
                }
                else
                {
                    newHeight = currentHeight + offsetY;
                    newWidth = newHeight * (currentWidth / currentHeight);
                }

                container.width(newWidth);
                container.height(newHeight);

                currentX = event.pageX;
                currentY = event.pageY;

            };

            let initResize = (event) => {

                event.stopPropagation();
                event.preventDefault();

                currentX = event.pageX;
                currentY = event.pageY;

                let viewport = $(window);

                viewport.mousemove(resize);
                viewport.mouseup(stopResize);

            };

            resizeButton.mousedown(initResize);

        },

        _dragAndDropEvent: function() {

            let container = this.element;

            let offset = null;

            let currentX = 0;
            let currentY = 0;

            let drop = (event) => {

                event.stopPropagation();

                let viewport = $(window);

                viewport.off("mousemove");
                viewport.off("mouseup");

            };

            let drag = (event) => {

                event.stopPropagation();
                event.preventDefault();

                let pointerX = event.pageX;
                let pointerY = event.pageY;

                let positionX = offset.left + (pointerX - currentX);
                let positionY = offset.top + (pointerY - currentY);

                container.offset({
                    left: positionX,
                    top: positionY
                });

            };

            let initDrag = (event) => {

                event.stopPropagation();
                event.preventDefault();

                offset = container.offset();

                currentX = event.pageX;
                currentY = event.pageY;

                let viewport = $(window);

                viewport.mousemove(drag);
                viewport.mouseup(drop);

            };

            container.mousedown(initDrag);

        },

        _closeEvent: function() {

            let closeButton = $("div#close-button");

            closeButton.click((event) => {

                event.stopPropagation();
                event.preventDefault();

                let component = $("div#talita-container");
                let button = $("div#talita-button");

                component.data("tasTalitaPlayer")
                         .destroy();

                button.show();

            });

        }

    });

    $.widget("tas.talita", {

        options: {},

        _create: function() {

            let container = $("<div>");

            container.attr("id", "talita-container");
           
            this.element.prepend(container);

            let button = $("<div>");

            button.attr("id", "talita-button");

            let buttonOptions = this.options.button;

            if (!buttonOptions || !buttonOptions.position || buttonOptions.position == "right")
                button.addClass("right");

            if (buttonOptions && buttonOptions.position && buttonOptions.position == "left")
                button.addClass("left");

            this.element.prepend(button);

            this._buttonClickEvent();

            this._scrollEvent();

        },

        _buttonClickEvent: function() {

            let button = $("div#talita-button");

            button.bind("click.talitaButton", (event) => {

                $("div#talita-container").talitaPlayer(this.options.player);
                $("div#talita-button").hide();

            });

        },

        _scrollEvent: function() {

            let button = $("div#talita-button");

            let iniScrollTop = 0;
            let iniScrollLeft = 0;

            $(window).bind("scroll.talitaButton", function(event) {

                let curScrollTop = $(this).scrollTop();
                let curScrollLeft = $(this).scrollLeft();

                let buttonTop = button.offset().top;
                let buttonLeft = button.offset().left;

                let newButtonTop = buttonTop + (curScrollTop - iniScrollTop);
                let newButtonLeft = buttonLeft + (curScrollLeft - iniScrollLeft);

                button.offset({
                    top: newButtonTop,
                    left: newButtonLeft
                });

                iniScrollTop = curScrollTop;
                iniScrollLeft = curScrollLeft;

            });

            $(window).trigger("scroll.talitaButton");

        },

        _destroy: function() {

        }

    });

}(jQuery));