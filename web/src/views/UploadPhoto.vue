<template>
    <div id="UploadPhoto">
          <div class="container">
              <form class="upload-image" action="#">
                  <img src="#"/>
                <div class="file-field input-field">
                  <div class="btn">
                    <span>File</span>
                    <input type="file">
                  </div>
                  <div class="file-path-wrapper">
                    <input class="file-path validate" type="text">
                  </div>
                </div>
              </form>


              <div class="row upload-data">
                <form class="col s12">
                  <div class="row">
                    <div class="input-field col s12">
                      <input placeholder="Placeholder" id="name" type="text" class="validate">
                      <label for="name">Name</label>
                    </div>
                  </div>

                  <div class="row">
                    <form class="col s12">
                      <div class="row">
                        <div class="input-field col s12">
                          <textarea id="textarea1" class="materialize-textarea"></textarea>
                          <label for="textarea1">Textarea</label>
                        </div>
                      </div>
                    </form>
                  </div>

                  <div class="row">
                    <div class="input-field col s12">
                      <input placeholder="Placeholder" id="first_name" type="text" class="validate">
                      <label for="first_name">First Name</label>
                    </div>
                  </div>
                </form>
              </div>
              </div>
    </div>
</template>

<script>
    import "@/less/uploadphoto.less"
    export default {
        name: "UploadPhoto",
    }
</script>
