

var Tweet = Backbone.Model.extend({});


var Tweets = Backbone.Collection.extend({
                                            initialize : function(){
                                                this._meta = {};  
                                                this.put('last_tweet_id', 0);
                                            },
                                            model : Tweet,
                                            
                                            url : function(){
                                                return '/fetch_tweets/?last_tweet_id='+this.get('last_tweet_id');
                                            },

                                            put: function(prop, value) {
                                                this._meta[prop] = value;
                                            },
                                            get: function(prop) {
                                                return this._meta[prop];
                                            }
                                            
});

var SingleTweet = Backbone.View.extend({
                                           tagName : "tr",
                                           render : function() {
                                               this.el.innerHTML = "<td>" + this.model.get('text') + "</td>";
                                               return this;   
                                           }
});

var TweetView = Backbone.View.extend({
                                       tagName : "tbody",
                                       initialize : function (options){
                                           this.tweets = new Tweets();
                                       },
                                       
                                       render : function(){
                                           var thisView = this;
                                           this.tweets.fetch({success : function(){ 
                                                                  thisView.tweets.each(
                                                                      function(tweet){
                                                                          $(thisView.el).append(new SingleTweet({ model : tweet}).render().el);    
                                                                      }, thisView);
                                                              }});
                                           
                                           return this;
                                       }
});

var AppView = Backbone.View.extend({
                                       
                                       initialize : function(options){
                                           this.app = new TweetView({});
                                           this.indicator = $('#tweetspinner');
                                       },

                                       events : {
                                           'click #tweetsbutton' : "fetch_more_tweets"
                                       },
                                       
                                       fetch_more_tweets : function(event){
                                           event.preventDefault();
                                           var thisView = this;
                                           this.app.tweets.fetch(
                                               {
                                                   beforeSend : function()
                                                   {
                                                     $('#tweetsbutton').attr("disabled", "disabled");
                                                     thisView.indicator.show();  
                                                   },
                                                   success : function ()
                                                   {
                                                       $('#tweetslist').append(thisView.app.render().el);
                                                   },
                                                   complete : function()
                                                   {
                                                       thisView.app.tweets.put('last_tweet_id', thisView.app.tweets.last().get('tweet_id'));
                                                       thisView.indicator.hide();
                                                       $('#tweetsbutton').removeAttr("disabled");
                                                   }
                                               });
                                           
                                       }
                                   });



