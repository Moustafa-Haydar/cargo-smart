<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;
use App\Models\User;

class ForgotPassword extends Mailable
{
    use Queueable, SerializesModels;
    public function __construct(
        public User $user,
        public string $url
    ) {
    }

    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Reset your password',
        );
    }

    public function content(): Content
    {
        return new Content(
            view: 'emails.forgotPassword',
            with: [
                'user' => $this->user,
                'url' => $this->url,
            ],
        );
    }

    /**
     * Get the attachments for the message.
     *
     * @return array<int, \Illuminate\Mail\Mailables\Attachment>
     */
    public function attachments(): array
    {
        return [];
    }

    public function build()
    {

        return
            $this->subject('Reset your password ')
                ->view('emails.forgotPassword');

    }
}


