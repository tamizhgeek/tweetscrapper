

var Tweet = Backbone.Model.extend({});


var Tweets = Backbone.Collection.extend({
                                            model : Tweet,
                                            url : '/fetch_tweets'
                                            
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
                                       initialize : function (){
                                           this.tweets = new Tweets();
                                       },
                                       
                                       render : function(){
                                           var thisView = this;
                                           this.tweets.fetch({success : function(){ 
                                                                  thisView.tweets.each(
                                                                      function(tweet){
                                                                          console.log(tweet.get('text'));
                                                                          $(thisView.el).append(new SingleTweet({ model : tweet}).render().el);    
                                                                      }, thisView);    
                                                              }});
                                           
                                           return this;
                                       }
});

var AppView = Backbone.View.extend({
                                       el : $('body'),
                                       initialize : function(){
                                           this.app = new TweetView();
                                           $('#tweetslist').append(this.app.render().el);
                                       },
                                       events : {
                                           'click #tweetsbutton' : "fetch_more_tweets"
                                       },
                                       
                                       fetch_more_tweets : function(){
                                           var thisView = this;
                                           this.app.tweets.fetch(
                                               {
                                                   success : function ()
                                                   {
                                                       $('#tweetslist').append(thisView.app.render().el);
                                                   }
                                               });
                                           
                                       }
                                   });



