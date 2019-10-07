module.ReceiptScreenWidget = module.ReceiptScreenWidget.include({
        send : function() {
            var self = this;
            var loaded = new $.Deferred();
            var order = this.pos.get_order().name;
            var records = new Model('pos.order').call('send_order', [order], {}, { shadow: false, timeout: 10000});
            records.then(function(result){
                var el = self.$('.message-send')
                el.empty();
                el.append('<h2>' + result + '</h2>');
            },function(err){
                loaded.reject(err);
            });
        },
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.button.send').click(function(){
                if (!self._locked) {
                    self.send();
                }
            });
        },
        show: function(){
            this._super();
            var self = this;
            this.$('.message-send').empty();
        },
    })