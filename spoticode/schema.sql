--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tr_fn_auto_calc_on_playlist_songs_count(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_auto_calc_on_playlist_songs_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
	IF TG_OP = 'INSERT' THEN
		UPDATE
			playlists 
		SET
			songs_local = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations
				WHERE 
					playlist_id = NEW.playlist_id
				)
		WHERE 
			playlist_id = NEW.playlist_id;
		
		UPDATE
			playlists 
		SET
			songs_spotify = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations spr
				JOIN songs s
					ON s.song_id = spr.song_id
				WHERE 
					spr.playlist_id = NEW.playlist_id
					AND s.spotify_link IS NOT NULL
				)
		WHERE 
			playlist_id = NEW.playlist_id;
		
		RETURN NEW;
		
	ELSIF TG_OP = 'DELETE' THEN
		UPDATE
			playlists 
		SET
			songs_local = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations
				WHERE 
					playlist_id = OLD.playlist_id
				)
		WHERE 
			playlist_id = OLD.playlist_id;
		
		UPDATE
			playlists 
		SET
			songs_spotify = (
				SELECT 
					COUNT(*)
				FROM
					song_playlist_relations spr
				JOIN songs s
					ON s.song_id = spr.song_id
				WHERE 
					spr.playlist_id = OLD.playlist_id
					AND s.spotify_link IS NOT NULL
				)
		WHERE 
			playlist_id = OLD.playlist_id;
		
		RETURN OLD;

	END IF;
   
END;
$$;


--
-- Name: tr_fn_auto_calc_songs_spotify(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_fn_auto_calc_songs_spotify() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

        UPDATE 
        	playlists 
        SET 
        	songs_spotify = (
            	SELECT 
            		COUNT(*)
            	FROM 
            		song_playlist_relations spr
            	JOIN songs s 
            		ON s.song_id = spr.song_id
            WHERE 
            	spr.playlist_id = playlists.playlist_id
            	AND s.spotify_link IS NOT NULL);

    RETURN NULL;
   
END;
$$;


--
-- Name: trg_fn_auto_update_all_after_albums(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_fn_auto_update_all_after_albums() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		
		-- All actions after INSERT on albums;
		IF TG_OP = 'INSERT' THEN
			
			-- 1) calc NEW artists
			UPDATE
				artists
			SET
				albums_count = (
					SELECT 
						COUNT(*)
					FROM
						albums
					WHERE 
						album_artist = NEW.album_artist
					)
			WHERE 
				artist_name = NEW.album_artist;
			
			-- 2) insert NEW links
			INSERT INTO albums_links (album_id)
				VALUES
					(NEW.album_id);
		
			RETURN NEW;
	
	-- All actions after UPDATE on albums;
	ELSIF TG_OP = 'UPDATE' THEN
	
		-- 1) calc OLD artists
		UPDATE
			artists
		SET
			albums_count = (
				SELECT 
					COUNT(*)
				FROM
					albums
				WHERE 
					album_artist = OLD.album_artist
				)
		WHERE 
			artist_name = OLD.album_artist;
		
		-- 2) calc NEW artists
		UPDATE
			artists
		SET
			albums_count = (
				SELECT 
					COUNT(*)
				FROM
					albums
				WHERE 
					album_artist = NEW.album_artist
				)
		WHERE 
			artist_name = NEW.album_artist;
		
		RETURN NEW;
		
	-- All actions after DELETE on albums;
	ELSIF TG_OP = 'DELETE' THEN
		
		-- 1) calc OLD artists
		UPDATE
			artists
		SET
			albums_count = (
				SELECT 
					COUNT(*)
				FROM
					albums
				WHERE 
					album_artist = OLD.album_artist
				)
		WHERE 
			artist_name = OLD.album_artist;
		
		RETURN OLD;

	END IF;
	END;
$$;


--
-- Name: trg_fn_auto_update_all_after_artists(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_fn_auto_update_all_after_artists() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		
		-- All actions after INSERT on artists;
		IF TG_OP = 'INSERT' THEN
			
			-- 1) check NEW pending
			IF EXISTS (
				SELECT 
					1
				FROM 
					artists 
				WHERE 
			        artist_name = NEW.artist_name
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					new_artist = FALSE
				WHERE
					main_artist = NEW.artist_name;
			ELSE
			    UPDATE 
			    	pending_songs 
			    SET 
			    	new_artist = TRUE 
			    WHERE 
			        main_artist = NEW.artist_name;
			END IF;
			
			-- 2) insert NEW links
			INSERT INTO artists_links (artist_id)
				VALUES
					(NEW.artist_id);
		
			RETURN NEW;
	
	-- All actions after UPDATE on artists;
	ELSIF TG_OP = 'UPDATE' THEN
	
		-- 1) check OLD pending
		IF EXISTS (
				SELECT 
					1
				FROM 
					artists 
				WHERE 
			        artist_name = OLD.artist_name
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					new_artist = FALSE
				WHERE
					main_artist = OLD.artist_name;
			ELSE
			    UPDATE 
			    	pending_songs 
			    SET 
			    	new_artist = TRUE 
			    WHERE 
			        main_artist = OLD.artist_name;
			END IF;
		
		-- 2) check NEW pending
		IF EXISTS (
				SELECT 
					1
				FROM 
					artists 
				WHERE 
			        artist_name = NEW.artist_name
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					new_artist = FALSE
				WHERE
					main_artist = NEW.artist_name;
			ELSE
			    UPDATE 
			    	pending_songs 
			    SET 
			    	new_artist = TRUE 
			    WHERE 
			        main_artist = NEW.artist_name;
			END IF;
		
		RETURN NEW;
		
	-- All actions after DELETE on artists;
	ELSIF TG_OP = 'DELETE' THEN
		
		-- 1) check OLD pending
		IF EXISTS (
			SELECT 
				1
			FROM 
				artists 
			WHERE 
				artist_name = OLD.artist_name
			) 
		THEN
			UPDATE
				pending_songs 
			SET
				new_artist = FALSE
			WHERE
				main_artist = OLD.artist_name;
		ELSE
		    UPDATE 
		    	pending_songs 
		    SET 
		    	new_artist = TRUE 
		    WHERE 
		        main_artist = OLD.artist_name;
		END IF;
		
		RETURN OLD;

	END IF;
	END;
$$;


--
-- Name: trg_fn_auto_update_all_after_pending(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_fn_auto_update_all_after_pending() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		
		-- All actions after INSERT on pending;
		IF TG_OP = 'INSERT' THEN
			
			-- 1) check NEW pending_artists
			IF EXISTS (
				SELECT 
					1
				FROM 
					artists 
				WHERE 
			        artist_name = NEW.main_artist
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					new_artist = FALSE
				WHERE
					main_artist = NEW.main_artist;
			ELSE
			    UPDATE 
			    	pending_songs 
			    SET 
			    	new_artist = TRUE 
			    WHERE 
			        main_artist = NEW.main_artist;
			END IF;
			
			-- 2) check NEW pending_songs
			IF EXISTS (
				SELECT 
					1
				FROM 
					songs 
				WHERE 
		        	song_title = NEW.song_title
		        	AND main_artist = NEW.main_artist
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					is_added = FALSE
				WHERE
					main_artist = NEW.main_artist;
			ELSE
			    UPDATE 
			    	pending_songs 
			    SET 
			    	is_added = TRUE 
			    WHERE 
			        main_artist = NEW.main_artist;
			END IF;
		
			-- 3) calc NEW groups
			UPDATE
				music_groups 
			SET
				pending_count = (
					SELECT 
						COUNT(*)
					FROM
						pending_songs
					WHERE 
						to_group = NEW.to_group
					)
			WHERE 
				group_name = NEW.to_group;
		
			RETURN NEW;
	
	-- All actions after UPDATE on pending;
	ELSIF TG_OP = 'UPDATE' THEN
	
		-- 1) check OLD pending_artists
		
		-- 2) check NEW pending_artists

		-- 3) check OLD pending_songs
		
		-- 4) check NEW pending_songs
	
		-- 5) calc OLD groups
		UPDATE
				music_groups 
			SET
				pending_count = (
					SELECT 
						COUNT(*)
					FROM
						pending_songs
					WHERE 
						to_group = OLD.to_group
					)
			WHERE 
				group_name = OLD.to_group;
		
		-- 6) calc NEW groups
		UPDATE
				music_groups 
			SET
				pending_count = (
					SELECT 
						COUNT(*)
					FROM
						pending_songs
					WHERE 
						to_group = NEW.to_group
					)
			WHERE 
				group_name = NEW.to_group;
		
			RETURN NEW;
		
		RETURN NEW;
		
	-- All actions after DELETE on pending;
	ELSIF TG_OP = 'DELETE' THEN
		
		-- 1) calc OLD groups
		UPDATE
				music_groups 
			SET
				pending_count = (
					SELECT 
						COUNT(*)
					FROM
						pending_songs
					WHERE 
						to_group = OLD.to_group
					)
			WHERE 
				group_name = OLD.to_group;
		
		RETURN OLD;

	END IF;
	END;
$$;


--
-- Name: trg_fn_auto_update_all_after_songs(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.trg_fn_auto_update_all_after_songs() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	BEGIN
		
		-- All actions after INSERT on pending;
		IF TG_OP = 'INSERT' THEN
		
		-- 1) calc NEW artists
		UPDATE
			artists
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					main_artist = NEW.main_artist
				)
		WHERE 
			artist_name = NEW.main_artist;
	
		-- 2) calc NEW groups
		UPDATE
			music_groups  
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					"group" = NEW."group"
				)
		WHERE 
			group_name = NEW."group";
	
		-- 3) calc NEW genres
		UPDATE
			genres 
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					genre = NEW.genre
				)
		WHERE 
			genre_name = NEW.genre;
		
		-- 4) check NEW pending
		IF EXISTS (
			SELECT 
				1
			FROM 
				songs 
			WHERE 
	        	song_title = NEW.song_title
	        	AND main_artist = NEW.main_artist
			) 
		THEN
			UPDATE
				pending_songs 
			SET
				is_added = TRUE
			WHERE
				song_title = NEW.song_title
	        	AND main_artist = NEW.main_artist;
	    ELSE
	    	UPDATE 
	    		pending_songs 
	    	SET 
	    		is_added = FALSE 
	    	WHERE 
	    		song_title = NEW.song_title
	        	AND main_artist = NEW.main_artist;
		END IF;
		
		RETURN NEW;
	
		-- All actions after UPDATE on pending;
		ELSIF TG_OP = 'UPDATE' THEN
		
			-- 1) calc OLD artists
			UPDATE
				artists
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						main_artist = OLD.main_artist
					)
			WHERE 
				artist_name = OLD.main_artist;
			
			-- 2) calc NEW artists
			UPDATE
				artists
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						main_artist = NEW.main_artist
					)
			WHERE 
				artist_name = NEW.main_artist;
		
			-- 3) calc OLD groups
			UPDATE
				music_groups  
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						"group" = OLD."group"
					)
			WHERE 
				group_name = OLD."group";
			
			-- 4) calc NEW groups
			UPDATE
				music_groups  
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						"group" = NEW."group"
					)
			WHERE 
				group_name = NEW."group";
		
			-- 5) calc OLD genres
			UPDATE
				genres 
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						genre = OLD.genre
					)
			WHERE 
				genre_name = OLD.genre;
			
			-- 6) calc NEW genres
			UPDATE
				genres 
			SET
				songs_count = (
					SELECT 
						COUNT(*)
					FROM
						songs
					WHERE 
						genre = NEW.genre
					)
			WHERE 
				genre_name = NEW.genre;
			
			-- 7) check OLD pending
			IF EXISTS (
				SELECT 
					1
				FROM 
					songs 
				WHERE 
		        	song_title = OLD.song_title
		        	AND main_artist = OLD.main_artist
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					is_added = TRUE
				WHERE
					song_title = OLD.song_title
		        	AND main_artist = OLD.main_artist;
		    ELSE
		    	UPDATE 
		    		pending_songs 
		    	SET 
		    		is_added = FALSE 
		    	WHERE 
		    		song_title = OLD.song_title
		        	AND main_artist = OLD.main_artist;
			END IF;
		
			-- 8) check NEW pending
			IF EXISTS (
				SELECT 
					1
				FROM 
					songs 
				WHERE 
		        	song_title = NEW.song_title
		        	AND main_artist = NEW.main_artist
				) 
			THEN
				UPDATE
					pending_songs 
				SET
					is_added = TRUE
				WHERE
					song_title = NEW.song_title
		        	AND main_artist = NEW.main_artist;
		    ELSE
		    	UPDATE 
		    		pending_songs 
		    	SET 
		    		is_added = FALSE 
		    	WHERE 
		    		song_title = NEW.song_title
		        	AND main_artist = NEW.main_artist;
			END IF;
			
			RETURN NEW;
	
	
	-- All actions after DELETE on pending;
	ELSIF TG_OP = 'DELETE' THEN
		
		-- 1) calc OLD artists
		UPDATE
			artists
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					main_artist = OLD.main_artist
				)
		WHERE 
			artist_name = OLD.main_artist;
	
		-- 2) calc OLD groups
		UPDATE
			music_groups  
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					"group" = OLD."group"
				)
		WHERE 
			group_name = OLD."group";
		
		-- 3) calc OLD genres
		UPDATE
			genres 
		SET
			songs_count = (
				SELECT 
					COUNT(*)
				FROM
					songs
				WHERE 
					genre = OLD.genre
				)
		WHERE 
			genre_name = OLD.genre;
		
		-- 4) check OLD pending
		IF EXISTS (
			SELECT 
				1
			FROM 
				songs 
			WHERE 
	        	song_title = OLD.song_title
	        	AND main_artist = OLD.main_artist
		) THEN
			UPDATE
				pending_songs 
			SET
				is_added = TRUE
			WHERE
				song_title = OLD.song_title
	        	AND main_artist = OLD.main_artist;
	    ELSE
	    	UPDATE 
	    		pending_songs 
	    	SET 
	    		is_added = FALSE 
	    	WHERE 
	    		song_title = OLD.song_title
	        	AND main_artist = OLD. main_artist;
		END IF;
		
		RETURN OLD;
	
	END IF;
   
END;
$$;


--
-- Name: album_tracks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.album_tracks (
    track_id character varying NOT NULL PRIMARY KEY,
    album_id character varying NOT NULL,
    track_num integer NOT NULL,
    track_name character varying NOT NULL,
    feat_artist character varying,
    song_id character varying,
    CONSTRAINT album_tracks_track_num_check CHECK ((track_num >= 0))
);


--
-- Name: albums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.albums (
    album_id character varying NOT NULL PRIMARY KEY,
    release_date date,
    album_name character varying NOT NULL,
    album_type character varying DEFAULT 'Unknown'::character varying NOT NULL,
    album_artist character varying NOT NULL
);


--
-- Name: albums_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.albums_links (
    album_id character varying NOT NULL PRIMARY KEY,
    spotify_link character varying(200),
    wikipedia_link character varying(200),
    rateyourmusic_link character varying(200)
);


--
-- Name: artists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artists (
    artist_id character varying(5) NOT NULL PRIMARY KEY,
    artist_name character varying NOT NULL,
    other_names character varying,
    songs_count integer DEFAULT 0 NOT NULL,
    albums_count integer DEFAULT 0 NOT NULL
);


--
-- Name: artists_links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artists_links (
    artist_id character varying(5) NOT NULL PRIMARY KEY,
    official_website character varying(200),
    spotify_link character varying(200),
    wikipedia_link character varying(200),
    rateyourmusic_link character varying(200)
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL PRIMARY KEY,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL PRIMARY KEY,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL PRIMARY KEY,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL PRIMARY KEY,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL PRIMARY KEY,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL PRIMARY KEY,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL PRIMARY KEY,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL PRIMARY KEY,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.songs (
    song_id character varying NOT NULL PRIMARY KEY,
    song_title character varying NOT NULL,
    feat_artist character varying,
    song_year integer,
    spotify_link character varying(200),
    album_id character varying,
    genre character varying(100),
    "group" character varying(100) DEFAULT 'Unspecified'::character varying NOT NULL,
    main_artist character varying NOT NULL
);


--
-- Name: genres; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.genres (
    id character varying NOT NULL PRIMARY KEY,
    genre_name character varying(100) NOT NULL,
    songs_count integer DEFAULT 0 NOT NULL,
    description text
);


--
-- Name: music_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.music_groups (
    id character varying NOT NULL PRIMARY KEY,
    group_name character varying(100) NOT NULL,
    songs_count integer DEFAULT 0 NOT NULL,
    pending_count integer DEFAULT 0 NOT NULL
);


--
-- Name: pending_songs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pending_songs (
    pending_id character varying NOT NULL PRIMARY KEY,
    song_title character varying NOT NULL,
    main_artist character varying NOT NULL,
    feat_artist character varying,
    is_added boolean DEFAULT false NOT NULL,
    new_artist boolean DEFAULT false NOT NULL,
    to_group character varying(100) DEFAULT 'Unspecified'::character varying NOT NULL
);


--
-- Name: playlists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playlists (
    playlist_id character varying NOT NULL PRIMARY KEY,
    playlist_name character varying NOT NULL,
    songs_local integer DEFAULT 0 NOT NULL,
    songs_spotify integer DEFAULT 0 NOT NULL,
    playlist_link character varying(200),
    playlist_image character varying(100),
    notes text,
    CONSTRAINT playlists_songs_local_check CHECK ((songs_local >= 0)),
    CONSTRAINT playlists_songs_spotify_check CHECK ((songs_spotify >= 0))
);


--
-- Name: song_playlist_relations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.song_playlist_relations (
    id character varying NOT NULL PRIMARY KEY,
    playlist_id character varying NOT NULL,
    song_id character varying NOT NULL
);


--
-- Name: task_comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_comments (
    comment_id character varying NOT NULL PRIMARY KEY,
    comment_text text NOT NULL,
    date_added timestamp with time zone NOT NULL,
    task_id character varying NOT NULL,
    "user" character varying(150) NOT NULL
);


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    task_id character varying NOT NULL PRIMARY KEY,
    date_created timestamp with time zone NOT NULL,
    last_modified timestamp with time zone NOT NULL,
    date_closed timestamp with time zone,
    task_name character varying(50) NOT NULL,
    related_app character varying DEFAULT 'Administration'::character varying NOT NULL,
    status character varying DEFAULT 'Not Started'::character varying NOT NULL,
    priority character varying DEFAULT 'Normal'::character varying NOT NULL,
    task_type character varying DEFAULT 'Bug'::character varying NOT NULL,
    description text NOT NULL,
    responsible character varying(150)
);


--
-- Name: view_show_songs_by_first_letter_artist; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.view_show_songs_by_first_letter_artist AS
 SELECT
        CASE
            WHEN (upper("left"((songs.main_artist)::text, 1)) = ANY (ARRAY['0'::text, '1'::text, '2'::text, '3'::text, '4'::text, '5'::text, '6'::text, '7'::text, '8'::text, '9'::text])) THEN '0-9'::text
            ELSE upper("left"((songs.main_artist)::text, 1))
        END AS first_letter,
    count(*) AS count
   FROM public.songs
  GROUP BY
        CASE
            WHEN (upper("left"((songs.main_artist)::text, 1)) = ANY (ARRAY['0'::text, '1'::text, '2'::text, '3'::text, '4'::text, '5'::text, '6'::text, '7'::text, '8'::text, '9'::text])) THEN '0-9'::text
            ELSE upper("left"((songs.main_artist)::text, 1))
        END
  ORDER BY
        CASE
            WHEN (upper("left"((songs.main_artist)::text, 1)) = ANY (ARRAY['0'::text, '1'::text, '2'::text, '3'::text, '4'::text, '5'::text, '6'::text, '7'::text, '8'::text, '9'::text])) THEN '0-9'::text
            ELSE upper("left"((songs.main_artist)::text, 1))
        END;


--
-- Name: albums tr_albums_iud; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_albums_iud AFTER INSERT OR DELETE OR UPDATE ON public.albums FOR EACH ROW EXECUTE FUNCTION public.trg_fn_auto_update_all_after_albums();


--
-- Name: song_playlist_relations tr_update_after_change_on_song_playlist_relations; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_update_after_change_on_song_playlist_relations AFTER INSERT OR DELETE ON public.song_playlist_relations FOR EACH ROW EXECUTE FUNCTION public.tr_fn_auto_calc_on_playlist_songs_count();


--
-- Name: artists trg_artists_dml_auto_check; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_artists_dml_auto_check AFTER INSERT OR DELETE OR UPDATE ON public.artists FOR EACH ROW EXECUTE FUNCTION public.trg_fn_auto_update_all_after_artists();


--
-- Name: pending_songs trg_pending_iud; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_pending_iud AFTER INSERT OR DELETE OR UPDATE ON public.pending_songs FOR EACH ROW EXECUTE FUNCTION public.trg_fn_auto_update_all_after_pending();


--
-- Name: songs trg_songs_iud; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_songs_iud AFTER INSERT OR DELETE OR UPDATE ON public.songs FOR EACH ROW EXECUTE FUNCTION public.trg_fn_auto_update_all_after_songs();


--
-- PostgreSQL database dump complete
--

