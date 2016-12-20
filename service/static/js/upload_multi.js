Vue.component('file-item', {
	template: '\
    <li>\
      {{ title }}\
      <button v-on:click="$emit(\'remove\')">X</button>\
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
