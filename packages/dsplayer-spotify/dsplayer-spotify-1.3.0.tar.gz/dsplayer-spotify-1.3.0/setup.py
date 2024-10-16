from setuptools import setup, find_packages

setup(
    name='dsplayer-spotify',  
    version='1.3.0',
    packages=find_packages(),
    install_requires=[
        'dsplayer',
        'yt-dlp',
        'spotipy'
    ],
    entry_points={
        'dsplayer.plugins': [
            'spotify = dsplayer_spotify.spotify:SpotifyPlugin',
        ],
    },
)