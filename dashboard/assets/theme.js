if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.theme_namespace = {
    toggleTheme: function(n_clicks, currentTheme) {
        const newTheme = (currentTheme === 'light') ? 'dark' : 'light';
        const cssClass = (newTheme === 'dark') ? 'dark-theme' : 'light-theme';
        
        return [cssClass, newTheme];
    }
};