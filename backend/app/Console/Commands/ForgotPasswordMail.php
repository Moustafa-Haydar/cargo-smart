<?php
namespace App\Console\Commands;
use Illuminate\Console\Command;
use App\Mail\ForgotPassword;
use App\Models\User;
use Illuminate\Support\Facades\Log;

class ForgotPasswordMail extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:forgot-password';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // debug
        Log::info(message: 'Starting invoice email job.');

        $user = User::where('email', 'moustafahaydar.eng@gmail.com')->first();

        // debug
        Log::info($user);

        if (!$user) {
            $this->error('user not found.');
            return;
        }

        // Mail::to($user->email)->send(new OrderInvoiceMail($user));
        // $this->info('Invoice email sent successfully.');

        // // debug
        // Log::info(message: 'Invoice email sent successfully');

        return;
    }
}
