import {MDCRipple} from '@material/ripple';
import {MDCDialog} from '@material/dialog';
import {MDCList} from '@material/list';
import {MDCSnackbar} from '@material/snackbar';

const BASE_JS = (function() {
  function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
      setTimeout(fn, 1);
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  } 
  let snackbar = undefined;
  let fab_dialog = undefined;
  let fab_list = undefined;
  let share_dialog = undefined;
  let share_list = undefined;  
  let pageContentElement = undefined;
  docReady(function(event) {  
    snackbar = new MDCSnackbar(document.querySelector('.mdc-snackbar'));
    if (messages){
      console.log("messages: ", messages);
      snackbar.open();
    }
    fab_dialog = new MDCDialog(document.querySelector('#fab-dialog'));
    fab_list = new MDCList(document.querySelector('#fab-dialog .mdc-list'));
    share_dialog = new MDCDialog(document.querySelector('#share-dialog'));
    share_list = new MDCList(document.querySelector('#share-dialog .mdc-list'));    
    pageContentElement = document.querySelector('.page-content');
    let all_btns = document.querySelectorAll('.mdc-button');
    for(var j=0; j<all_btns.length; j++){
      var buttonRipple = new MDCRipple(all_btns[j]);
    }
  });

  class SnackBar{
    constructor(text){
      document.querySelector('#snackbar').innerHTML = text;
    }
    open(){
      snackbar.open();
    }
  }

  const getUrlParameter = function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1);
    let sURLVariables = sPageURL.split('&');
    let sParameterName = null;
    for (var i = 0; i < sURLVariables.length; i++) {
      sParameterName = sURLVariables[i].split('=');
      if (sParameterName[0] === sParam) {
          return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
      }
    }
  };

  class FabDialog{
    constructor(title, form, innerHTML, accept_btn, close_btn, openEventCallback, closeEventCallback) {
      document.querySelector('#fab-confirmation-dialog-title').textContent = title || 'Title';
      if(form!=undefined){
        var dialog_form = document.querySelector('#fab-dialog-form');
        var form_method = form['method'];
        if(form_method!=undefined){
          dialog_form.setAttribute('method', form_method);
        }      
        var form_action = form['action'];
        if(form_action!=undefined){
          dialog_form.setAttribute('action', form_action);
        }      
      }
      if(innerHTML!=undefined){
        document.querySelector('#fab-dialog-innerHTML').innerHTML = innerHTML || '';
      }
      if (accept_btn!=undefined){
        var accept_action_btn = document.querySelector('#fab-dialog button[data-mdc-dialog-action="accept"]');
        var accept_btn_text = accept_btn['text'];
        if(accept_btn_text!=undefined){
          accept_action_btn.textContent = accept_btn_text || 'OK';  
        }
        var accept_btn_type = accept_btn['type'];
        if(accept_btn_type!=undefined){
          accept_action_btn.setAttribute('type', accept_btn_type);
        }
        var accept_btn_onclick = accept_btn['onclick'];
        if(accept_btn_onclick!=undefined){
          accept_action_btn.setAttribute('onclick', accept_btn_onclick);
        }      
      }
      if (close_btn!=undefined){
        var close_action_btn = document.querySelector('#fab-dialog button[data-mdc-dialog-action="close"]');
        var close_btn_text = close_btn['text'];
        if(close_btn_text!=undefined){
          close_action_btn.textContent = close_btn_text || 'CANCEL';  
        }
        var close_btn_type = close_btn['type'];
        if(close_btn_type!=undefined){
          close_action_btn.setAttribute('type', close_btn_type);
        }
        var close_btn_onclick = close_btn['onclick'];
        if(close_btn_onclick!=undefined){
          close_action_btn.setAttribute('onclick', close_btn_onclick);
        }          
      }

      var openEventListener = function(evt){
        fab_list.layout();
        pageContentElement.setAttribute('aria-hidden', 'true'); 
        fab_dialog.unlisten("MDCDialog:opened", openEventListener);
        try{
          openEventCallback(evt);
        }catch(e){
          console.error("Error 1 : ", e);
        }
      }
      var closeEventListener = function(evt){
        pageContentElement.removeAttribute('aria-hidden');     
        fab_dialog.unlisten("MDCDialog:closing", closeEventListener);
        try{
          closeEventCallback(evt);
        }catch(e){
          console.error("Error 2 : ", e);
        }
      }  

      fab_dialog.listen("MDCDialog:opened", openEventListener);
      fab_dialog.listen("MDCDialog:closing", closeEventListener);  
    }  

    open(){
      fab_dialog.open();
    }
  }

  class ShareDialog{
    constructor(title, form, innerHTML, accept_btn, close_btn, openEventCallback, closeEventCallback) {
      document.querySelector('#share-confirmation-dialog-title').textContent = title || 'Title';
      if(form!=undefined){
        var dialog_form = document.querySelector('#share-dialog-form');
        var form_method = form['method'];
        if(form_method!=undefined){
          dialog_form.setAttribute('method', form_method);
        }      
        var form_action = form['action'];
        if(form_action!=undefined){
          dialog_form.setAttribute('action', form_action);
        }      
      }
      if(innerHTML!=undefined){
        document.querySelector('#share-dialog-innerHTML').innerHTML = innerHTML || '';
      }
      if (accept_btn!=undefined){
        var accept_action_btn = document.querySelector('#share-dialog button[data-mdc-dialog-action="accept"]');
        var accept_btn_text = accept_btn['text'];
        if(accept_btn_text!=undefined){
          accept_action_btn.textContent = accept_btn_text || 'OK';  
        }
        var accept_btn_type = accept_btn['type'];
        if(accept_btn_type!=undefined){
          accept_action_btn.setAttribute('type', accept_btn_type);
        }
        var accept_btn_onclick = accept_btn['onclick'];
        if(accept_btn_onclick!=undefined){
          accept_action_btn.setAttribute('onclick', accept_btn_onclick);
        }      
      }
      if (close_btn!=undefined){
        var close_action_btn = document.querySelector('#share-dialog button[data-mdc-dialog-action="close"]');
        var close_btn_text = close_btn['text'];
        if(close_btn_text!=undefined){
          close_action_btn.textContent = close_btn_text || 'CANCEL';  
        }
        var close_btn_type = close_btn['type'];
        if(close_btn_type!=undefined){
          close_action_btn.setAttribute('type', close_btn_type);
        }
        var close_btn_onclick = close_btn['onclick'];
        if(close_btn_onclick!=undefined){
          close_action_btn.setAttribute('onclick', close_btn_onclick);
        }          
      }

      var openEventListener = function(evt){
        share_list.layout();
        pageContentElement.setAttribute('aria-hidden', 'true'); 
        share_dialog.unlisten("MDCDialog:opened", openEventListener);
        try{
          openEventCallback(evt);
        }catch(e){
          console.error("Error 1 : ", e);
        }
      }
      var closeEventListener = function(evt){
        pageContentElement.removeAttribute('aria-hidden');     
        share_dialog.unlisten("MDCDialog:closing", closeEventListener);
        try{
          closeEventCallback(evt);
        }catch(e){
          console.error("Error 2 : ", e);
        }
      }  

      share_dialog.listen("MDCDialog:opened", openEventListener);
      share_dialog.listen("MDCDialog:closing", closeEventListener);  
    }  

    open(){
      share_dialog.open();
    }
  }

  return {docReady : docReady, getUrlParameter : getUrlParameter, FabDialog : FabDialog, ShareDialog : ShareDialog, SnackBar : SnackBar}
})()

export { BASE_JS };