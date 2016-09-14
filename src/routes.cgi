#!/usr/bin/perl

use strict;

use JSON;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Data::Dumper;
use Math::Geometry::Planar;



print "Content-Type: text/json\r\n";
print "Access-Control-Allow-Origin: *\r\n";
print "\r\n";



# orig dest

# 1. call Maps api type=walking (orig, dest)
# 2. for each segment lat,long
# 3. call places API on (lat, long) with radius=500
# 3a. split up long line segments
# 4. for each place, associate place with a segment
# 5. compute safety score for each segment
# 6. sum safety scores for each route
# 7. sort routes by safety score
# 8. http rest api to return json to front end


# long segment:
#   origin=place_id:ChIJnUwiTr1YwokRs-Hc0hBqAcA
#   destination=place_id:ChIJSRfEz-JYwokRA5qI_DOzkKg

# 366 columbus ave to 781 lexington
# origin=place_id:ChIJa_tM0I5YwokRj9EdR3IycDQ
# destination=place_id:Eio3ODEgTGV4aW5ndG9uIEF2ZSwgTmV3IFlvcmssIE5ZIDEwMDY1LCBVU0E

my $origin = 'place_id:ChIJ_bbmI31YwokRKM_Qj3DXcwE';
my $destination = 'place_id:ChIJA-d80JRZwokRfYrdNAwe1qg';

#my $origin = 'place_id:ChIJa_tM0I5YwokRj9EdR3IycDQ';
#my $destination='place_id:Eio3ODEgTGV4aW5ndG9uIEF2ZSwgTmV3IFlvcmssIE5ZIDEwMDY1LCBVU0E';

#my $origin = 'place_id:ChIJnUwiTr1YwokRs-Hc0hBqAcA';
#my $destination = 'place_id:ChIJSRfEz-JYwokRA5qI_DOzkKg';


if ( $ENV{QUERY_STRING} =~ /origin=([^&]+)/ )
{
    $origin = $1;
}

if ( $ENV{QUERY_STRING} =~ /destination=([^&]+)/ )
{
    $destination = $1;
}

my $pinpoints =
{
    '3b9ffa24653d9626' =>
    {
        crimes => [ 17, 5, 3 ],
        safety => [ 3.3, 6.4, 5.2 ],
        pinpoints =>
            [
                {
                   "tag" => "crime",
                   "lat" => 40.759081,
                   "lng" => -74.002748
                },
                {
                   "tag" => "establishment",
                   "lat" => 40.743509,
                   "lng" => -74.003477
                },
                {
                   "tag" => "crime",
                   "lat" => 40.757098,
                   "lng" => -74.002576
                },
                {
                   "tag" => "crime",
                   "lat" => 40.754173,
                   "lng" => -74.006653
                },
                {
                   "tag" => "establishment",
                   "lat" => 40.759471,
                   "lng" => -73.988199
                },
                {
                   "tag" => "establishment",
                   "lat" => 40.747898,
                   "lng" => -74.000430
                },
                {
                   "tag" => "crime",
                   "lat" => 40.753295,
                   "lng" => -73.996310
                },
            ],
    },
};



my $api_key = 'AIzaSyAs4DpgjVRXUMRvj3oTxdXHSaB2T0O17wM';

my $places;
my $segments;
my $to_call = {};

my $path = call_url( "https://maps.googleapis.com/maps/api/directions/json?origin=$origin&destination=$destination&alternatives=true&mode=walking&key=$api_key" );

compute_route_id( $path );
get_places( $path );
fit_places_to_segments();
find_best_title($path);
format_output( $path );


exit(0);

sub compute_route_id
{
    my ( $path ) = @_;

    foreach my $route ( @{ $path->{routes} } )
    {
        my $inst;
        foreach my $leg ( @{ $route->{legs} } )
        {
            foreach my $step ( @{ $leg->{steps} } )
            {
                $inst .= $step->{html_instructions};
            }

            last;
        }

        $route->{route_id} = substr( md5_hex( $inst ), 0, 16 );
    }
}

sub find_best_title
{
    my ( $path ) = @_;

    my %seen;

    foreach my $route ( @{ $path->{routes} } )
    {
        foreach my $leg ( @{ $route->{legs} } )
        {
            foreach my $step ( @{ $leg->{steps} } )
            {
                my $inst = $step->{html_instructions};

                if ( $inst =~ m,(?:on|onto|toward) <b>(.*?)</b>, )
                {
                    next if $seen{ $1 };
                    $route->{titles}->{ $1 } += $step->{distance}->{value};
                }
            }

            foreach my $title ( keys %{ $route->{titles} } )
            {
                $seen{ $title } = 1;
            }

            last;
        }

        foreach my $title ( sort { $route->{titles}->{$b} <=> $route->{titles}->{$a} } keys %{ $route->{titles} } )
        {
            $route->{best_title} = 'via ' . $title;
            last;
        }
    }

    #print Dumper($path->{routes} );
}

sub format_output
{
    my ( $path ) = @_;

    my @routes;

    my $route_id = $path->{routes}->[0]->{route_id};
    my $pp;
    if ( defined $pinpoints->{ $route_id } )
    {
       $pp = $pinpoints->{ $route_id };
    }

    my $routenum = 0;
    foreach my $route ( @{ $path->{routes} } )
    {
        my $ref;

        $ref->{title} = $route->{best_title};
        $ref->{route_id} = $route->{route_id};

        foreach my $leg ( @{ $route->{legs} } )
        {
            $ref->{distance} = $leg->{distance}->{text};
            $ref->{time} = $leg->{duration}->{text};
            #$ref->{openNow} = 13;
            $ref->{crimes} = 5;

            if ( defined $pp && $pp->{crimes}->[ $routenum ] )
            {
                $ref->{crimes} = $pp->{crimes}->[ $routenum ];
            }

            if ( defined $pp && $pp->{safety}->[ $routenum ] )
            {
                $ref->{safety} = $pp->{safety}->[ $routenum ];
            }

            $ref->{crimes} = $pinpoints->{ '3b9ffa24653d9626' }->{crimes}->[ $routenum ];
            $ref->{safety} = $pinpoints->{ '3b9ffa24653d9626' }->{safety}->[ $routenum ];

            my $inst = parse_inst( $leg->{steps}->[0]->{html_instructions} );

            my $coord =
                {
                    lat => $leg->{steps}->[0]->{start_location}->{lat},
                    lng => $leg->{steps}->[0]->{start_location}->{lng},
                    text => $inst,
                };

            push @{ $ref->{waypoints} }, $coord;

            foreach my $step ( @{ $leg->{steps} } )
            {
                my $inst = parse_inst( $step->{html_instructions} );

                my $coord =
                    {
                        lat => $step->{end_location}->{lat},
                        lng => $step->{end_location}->{lng},
                        text => $inst,
                    };

                push @{ $ref->{waypoints} }, $coord;

                my $s = $step->{start_location}->{lat} . ',' . $step->{start_location}->{lng} . ',' .
                    $step->{end_location}->{lat} . ',' . $step->{end_location}->{lng};

                $ref->{openNow} += $segments->{$s};
            }

            if ( !defined $ref->{safety} )
            {
                $ref->{safety} = 7.5;
                $ref->{safety} = $ref->{openNow} / ( $leg->{distance}->{value} / 7000 );
                $ref->{safety} = 10 if $ref->{safety} > 10;
                $ref->{safety} = sprintf( "%.1f", $ref->{safety} );
                #$ref->{distval} = $leg->{distance}->{value};
            }

            last;
        }

        push @routes, $ref;
        $routenum++;
    }

    my $out =
        {
            routes => \@routes,
            query_string => $ENV{QUERY_STRING},
        };

    $out->{pinpoints} = $pp->{pinpoints} if defined $pp && defined $pp->{pinpoints};
    $out->{pinpoints} = $pinpoints->{ '3b9ffa24653d9626' }->{pinpoints};

    my $json = to_json( $out, { ascii => 1, pretty => 1 } );

    print $json, "\n";
}

sub parse_inst
{
    my ( $s ) = @_;

    $s =~ s,</?b>,,g;
    $s =~ s,<div[^>]*>.*?<\/div>,,g;

    return $s;
}

sub get_places
{
    my ( $path ) = @_;

    foreach my $route ( @{ $path->{routes} } )
    {
        foreach my $leg ( @{ $route->{legs} } )
        {
            add_to_call( $leg->{steps}->[0]->{start_location} );

            foreach my $step ( @{ $leg->{steps} } )
            {
                add_to_call( $step->{end_location} );
                add_segment( $step );
            }
        }
    }

    foreach my $coord ( keys %$to_call )
    {
        my $ret = call_url( "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=$coord&radius=100&key=AIzaSyBNNBtO4qu8cNq9QMJ7ti7WaFmRe55k4IY" );

        foreach my $place ( @{ $ret->{results} } )
        {
            next if $place->{vicinity} !~ /,/;      # skip places like "New York" that don't have a street adddress
            next if !defined $place->{opening_hours};

            my $latlng = $place->{geometry}->{location}->{lat} . ',' . $place->{geometry}->{location}->{lng};

            my $street = $place->{vicinity};
            $street =~ s/^\d+\s*//;
            my $streetnum = $place->{vicinity};
            $streetnum =~ s/\s.*$//;

            $place->{x_street} = $street;
            $place->{x_streetnum} = $streetnum;

            $places->{ $latlng } = $place;
        }

#        foreach my $place ( sort { $a->{x_street} cmp $b->{x_street} || $a->{x_streetnum} <=> $b->{x_streetnum} } values %$places )
#        {
#            my $latlng = $place->{geometry}->{location}->{lat} . ',' . $place->{geometry}->{location}->{lng};
#
#            print sprintf( "%-40s %-40s  %s\n", $place->{name}, $place->{vicinity}, $latlng );
#        }
    }
}

sub add_segment
{
    my ( $step ) = @_;

    my $s = $step->{start_location}->{lat} . ',' . $step->{start_location}->{lng} . ',' .
            $step->{end_location}->{lat} . ',' . $step->{end_location}->{lng};

    $segments->{$s} = 0;
}

sub add_to_call
{
    my ( $loc ) = @_;

    my $s = $loc->{lat} . ',' . $loc->{lng};

    $to_call->{$s} = 0;
}

sub fit_places_to_segments
{
    foreach my $place ( keys %$places )
    {
        my ( $placey, $placex ) = split( /,/, $place );

        my $point = [ $placex, $placey ];

        foreach my $segment ( keys %$segments )
        {
            my ( $origy, $origx, $desty, $destx ) = split( /,/, $segment );

            my $l1 = [ $origx, $origy ];
            my $l2 = [ $destx, $desty ];

            #print STDERR "placex=$placex placey=$placey origx=$origx origy=$origy destx=$destx desty=$desty\n";

            my $dist = DistanceToSegment( [ $l1,$l2,$point ]);
            $dist = abs($dist);

            my $pref = $places->{$place};

            if ( !defined $pref->{closest_segment} || $dist < $pref->{closest_segment_dist} )
            {
                $pref->{closest_segment} = $segment;
                $pref->{closest_segment_dist} = $dist;
            }
        }
    }

    foreach my $place ( sort { $a->{closest_segment_dist} <=> $b->{closest_segment_dist} } values %$places )
    {
        if ( $place->{closest_segment_dist} < 0.0002 )
        {
            $segments->{ $place->{closest_segment} }++;
        }

        #print "name: ", $place->{name}, "\n";
        #print "distance: ", $place->{closest_segment_dist}, "\n";
        #my ( $a, $b, $c, $d ) = split( /,/, $place->{closest_segment} );
        #print "https://www.google.com/maps/dir/${a},${b}/${c},${d}/\n";
        ##print "closest_segment: ", $place->{closest_segment}, "\n";
        #print "\n";
    }

    #print Dumper($places);
}

sub show_pretty
{
    my ( $ref ) = @_;

    my $numroutes;
    $numroutes = scalar( @{ $ref->{routes} } ) if defined $ref->{routes};

    print "numroutes = $numroutes\n";

    my $nroute;
    foreach my $route ( @{ $ref->{routes} } )
    {
        $nroute++;
        print "route $nroute:\n";

        foreach my $leg ( @{ $route->{legs} } )
        {
            foreach my $step ( @{ $leg->{steps} } )
            {
                my $inst = $step->{html_instructions};
                $inst =~ s,</?b>,,g;
                $inst =~ s,<div[^>]*>.*?<\/div>,,g;
                #print "    ", $inst, "\n";

                print sprintf( "   %30s  ", print_latlng( $step->{start_location} ) );
                print sprintf( " %-50s ", $inst );
                print sprintf( "   %30s ", print_latlng( $step->{end_location} ) );
                print " dist=", $step->{distance}->{value}, "\n";
            }
            print "\n";
        }
    }
}

sub print_latlng
{
    my( $loc ) = @_;

    return $loc->{lat} . ',' . $loc->{lng};
}


sub call_url
{
    my ( $url ) = @_;

    my $hex = substr( md5_hex( $url ), 0, 16 );

    if ( ! -f "/home/skrenta/www/safetycache/$hex.json" )
    {
        #print STDERR "curl -s -f -o /home/skrenta/www/safetycache/$hex.json \"$url\"\n";

        `curl -s -f -o /home/skrenta/www/safetycache/$hex.json "$url"`;
    }

    open( JSON, "</home/skrenta/www/safetycache/$hex.json" ) or return;

    my $json;
    while ( my $line = <JSON> )
    {
        $json .= $line;
    }

    close( JSON );

    my $ref = decode_json( $json );

    return $ref;
}



#curl 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7217754,-73.9878745&opennow&radius=1500&type=restaurant&key=AIzaSyBNNBtO4qu8cNq9QMJ7ti7WaFmRe55k4IY'

#curl 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7217754,-73.9878745&opennow&radius=500&key=AIzaSyBNNBtO4qu8cNq9QMJ7ti7WaFmRe55k4IY'

#curl 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7217754,-73.9878745&opennow&type=hotel&radius=500&key=AIzaSyBNNBtO4qu8cNq9QMJ7ti7WaFmRe55k4IY'

#curl 'https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&alternatives=true&avoid=highways&mode=bicycling&key=AIzaSyAs4DpgjVRXUMRvj3oTxdXHSaB2T0O17wM'

#curl 'https://maps.googleapis.com/maps/api/directions/json?origin=place_id:ChIJdfuappxZwokRf_gWCLv9f5g&destination=place_id:ChIJx8sGD4FZwokRy6hAmRfzwqg&alternatives=true&mode=walking&key=AIzaSyAs4DpgjVRXUMRvj3oTxdXHSaB2T0O17wM'

#curl 'https://maps.googleapis.com/maps/api/directions/json?origin=place_id:ChIJnUwiTr1YwokRs-Hc0hBqAcA&destination=place_id:ChIJSRfEz-JYwokRA5qI_DOzkKg&alternatives=true&mode=walking&key=AIzaSyAs4DpgjVRXUMRvj3oTxdXHSaB2T0O17wM'


exit(0);
