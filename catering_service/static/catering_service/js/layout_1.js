import {MDCTopAppBar} from '@material/top-app-bar';
import {MDCDrawer} from "@material/drawer";
import {MDCRipple} from '@material/ripple';
import {BASE_JS} from "../../../../catering_service/static/catering_service/js/base"

const Layout1 = (function() {
  let fabRipple = undefined;
  let share = undefined;
  BASE_JS.docReady(function(event) { 
    const drawer = MDCDrawer.attachTo(document.querySelector('.mdc-drawer'));
    const topAppBar = MDCTopAppBar.attachTo(document.querySelector('.mdc-top-app-bar'));
    fabRipple = new MDCRipple(document.querySelector('.mdc-fab'));
    var share_el = document.querySelector('.mdc-top-app-bar__section--align-end .mdc-top-app-bar__action-item[aria-label="Share"]');
    share = new MDCRipple(share_el);    
    topAppBar.setScrollTarget(document.getElementById('main-content'));
    topAppBar.listen('MDCTopAppBar:nav', () => {
      drawer.open = !drawer.open;
    });

    const listEl = document.querySelector('.mdc-drawer .mdc-list');
    const mainContentEl = document.querySelector('.main-content');

    listEl.addEventListener('click', (event) => {
      try{
        drawer.open = false;
        mainContentEl.querySelector('input, button').focus();
      }catch(e){
        mainContentEl.focus();
      }
    });

    document.body.addEventListener('MDCDrawer:closed', () => {
      try{
        mainContentEl.querySelector('input, button').focus();
      }catch(e){
        mainContentEl.focus();
      }  
    });






  })
  

  class FabBtn{
      constructor(btn_name, btn_icon) {
      document.querySelector('.mdc-fab__label').textContent = btn_name || 'Create';
      document.querySelector('.mdc-fab__icon').textContent = btn_icon || 'add';
    }  

    open(callback){
      fabRipple.listen('click', () => {
        callback();
      });
    }
  }

  class ShareBtn{
    constructor(){

    }
    open(callback){
      share.listen('click', () => {
        callback();
      });
    }    
  }

  return {FabBtn : FabBtn, ShareBtn : ShareBtn}
})()  

  

export { Layout1 };
