Vue.component('file-item', {
	template: '\
    <li>\
			<div class="row">\
			<div class="col-sm-2">\
      <button v-on:click="$emit(\'remove\')" class="btn btn-danger">Remove</button>\
			</div>\
			<div class="col-sm-9 upload_items">\
			<p>{{ title }}</p>\
			</div>\
			</div>\
    </li>\
  ',
	props: ['title']
})
new Vue({
	el: '#file-list',
	data: {
		newFileText: '',
		files: []
	},
	methods: {
		addNewFile: function() {
			var uploadFile = this.newFileText.split('\\').pop()
			this.files.push(uploadFile)
			this.newFileText = ''
		}
	}
})
