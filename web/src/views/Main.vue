<template>
    <div id="Main">
        <!-- Dropdown Structure -->
        <ul id="dropdown1" class="dropdown-content">
          <li><a href="#!">one</a></li>
          <li><a href="#!">two</a></li>
          <li class="divider"></li>
          <li><a href="#!">three</a></li>
        </ul>
        <nav>
          <div class="nav-wrapper">
            <a href="#!" class="brand-logo">Rainbow</a>
            <ul class="right hide-on-med-and-down">
              <li><router-link to="/photo">Components</router-link></li>
              <li><a href="badges.html">Components</a></li>
              <!-- Dropdown Trigger -->
              <li><a class="dropdown-trigger" href="#!" data-target="dropdown1">Dropdown<i class="material-icons right">arrow_drop_down</i></a></li>
            </ul>
          </div>
        </nav>

        <div class="slider">
          <ul class="slides">
            <li>
              <img src="http://h2.ioliu.cn/bing/BrightonSnow_ZH-CN0309526170_1920x1080.jpg"> <!-- random image -->
              <div class="caption center-align">
                <h3>This is our big Tagline!</h3>
                <h5 class="light grey-text text-lighten-3">Here's our small slogan.</h5>
              </div>
            </li>
            <li>
              <img src="http://h2.ioliu.cn/bing/SierraNevada_ZH-CN0564237735_1920x1080.jpg"> <!-- random image -->
              <div class="caption left-align">
                <h3>Left Aligned Caption</h3>
                <h5 class="light grey-text text-lighten-3">Here's our small slogan.</h5>
              </div>
            </li>
            <li>
              <img src="http://h2.ioliu.cn/bing/RedFrontMacaw_ZH-CN6432596112_1920x1080.jpg?imageslim"> <!-- random image -->
              <div class="caption right-align">
                <h3>Right Aligned Caption</h3>
                <h5 class="light grey-text text-lighten-3">Here's our small slogan.</h5>
              </div>
            </li>
            <li>
              <img src="http://h2.ioliu.cn/bing/DiamondBeach_ZH-CN3165398805_800x480.jpg"> <!-- random image -->
              <div class="caption center-align">
                <h3>This is our big Tagline!</h3>
                <h5 class="light grey-text text-lighten-3">Here's our small slogan.</h5>
              </div>
            </li>
          </ul>
        </div>

        <div class="carousel carousel-slider center">
          <div class="carousel-fixed-item center">
            <a class="btn waves-effect white grey-text darken-text-2">button</a>
          </div>
          <div class="carousel-item red white-text" href="#one!">
            <h2>First Panel</h2>
            <p class="white-text">This is your first panel</p>
          </div>
          <div class="carousel-item amber white-text" href="#two!">
            <h2>Second Panel</h2>
            <p class="white-text">This is your second panel</p>
          </div>
          <div class="carousel-item green white-text" href="#three!">
            <h2>Third Panel</h2>
            <p class="white-text">This is your third panel</p>
          </div>
          <div class="carousel-item blue white-text" href="#four!">
            <h2>Fourth Panel</h2>
            <p class="white-text">This is your fourth panel</p>
          </div>
        </div>

        <footer class="page-footer">
          <div class="container">
            <div class="row">
              <div class="col l6 s12">
                <h5 class="white-text">Footer Content</h5>
                <p class="grey-text text-lighten-4">You can use rows and columns here to organize your footer content.</p>
              </div>
              <div class="col l4 offset-l2 s12">
                <h5 class="white-text">Links</h5>
                <ul>
                  <li><a class="grey-text text-lighten-3" href="#!">Link 1</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Link 2</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Link 3</a></li>
                  <li><a class="grey-text text-lighten-3" href="#!">Link 4</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div class="footer-copyright">
            <div class="container">
            © 2020 Copyright Rainbow
            <a class="grey-text text-lighten-4 right" href="https://beian.miit.gov.cn">桂ICP备17011922号-1</a>
            </div>
          </div>
        </footer>
    </div>
</template>

<script>
    import '@/less/main.less'
    window.$ = window.jQuery = require('jquery');
    export default {
        name: "Main",
        mounted() {
            window.jQuery(document).ready(function(){
                window.jQuery(".dropdown-trigger").dropdown();
                window.jQuery('.slider').slider();
            });

            window.jQuery('.carousel.carousel-slider').carousel({
                fullWidth: true,
                indicators: true,
            });
        },
    }
</script>

<style scoped>

</style>